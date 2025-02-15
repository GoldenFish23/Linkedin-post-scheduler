from flask import Blueprint, redirect, request, jsonify, url_for, session
import os
from datetime import datetime, timedelta
import requests
from flask import current_app
from dotenv import load_dotenv
from models import db, User
import logging

# Load environment variables
load_dotenv()

linkedin_bp = Blueprint("linkedin", __name__)

# LinkedIn OAuth URLs
AUTHORIZATION_URL = "https://www.linkedin.com/oauth/v2/authorization"
TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"
USERINFO_URL = "https://api.linkedin.com/v2/userinfo"
POST_URL = "https://api.linkedin.com/v2/ugcPosts"

# App credentials
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = "your-linkedin-callback-link"  # Replace it with your linkedin callback link
SCOPE = "openid profile email w_member_social"  # Make sure these scopes are alloted to Linkedin API

logging.basicConfig(level=logging.INFO)

@linkedin_bp.route("/login")
def login():
    """Redirect user to LinkedIn login page."""
    auth_url = (
        f"{AUTHORIZATION_URL}?response_type=code"
        f"&client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope={SCOPE}"
    )
    return redirect(auth_url)

@linkedin_bp.route("/linkedin/callback") # This should match your linkedin callback link
def callback():
    """Handle LinkedIn OAuth callback and fetch user details."""
    code = request.args.get("code")
    if not code:
        return jsonify({"error": "No Authorization Code Received"}), 400

    # Exchange code for access token
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }

    try:
        response = requests.post(TOKEN_URL, data=data)
        response.raise_for_status()
        token_data = response.json()
    except requests.RequestException as e:
        logging.error(f"Failed to get Access Token: {e}")
        return jsonify({"error": "Failed to get Access Token"}), 500

    if "access_token" not in token_data:
        return jsonify({"error": "Invalid LinkedIn response", "details": token_data}), 400

    access_token = token_data["access_token"]
    refresh_token = token_data.get("refresh_token", None)

    # Fetch user info
    headers = {"Authorization": f"Bearer {access_token}"}

    try:
        userinfo_response = requests.get(USERINFO_URL, headers=headers)
        userinfo_response.raise_for_status()
        userinfo = userinfo_response.json()
    except requests.RequestException as e:
        logging.error(f"Failed to get User Info: {e}")
        return jsonify({"error": "Failed to get User Info"}), 500

    first_name = userinfo.get("given_name", "Unknown")
    last_name = userinfo.get("family_name", "Unknown")
    email = userinfo.get("email", "Unknown")
    linkedin_id = userinfo.get("sub")

    with current_app.app_context():  # Ensure database queries run inside app context
        user = User.query.filter_by(email=email).first()

        if not user:
            user = User(first_name=first_name, linkedin_id=linkedin_id, last_name=last_name, email=email)
            db.session.add(user)

        # Update LinkedIn tokens
        user.linkedin_id = linkedin_id
        user.linkedin_access_token = access_token
        user.linkedin_refresh_token = refresh_token

        db.session.commit()
        db.session.refresh(user)  # Ensure user remains bound after commit

    session["user_id"] = user.id  # This should now work without DetachedInstanceError
    return redirect(url_for("dashboard"))


def refresh_linkedin_token(user):
    """Refreshes the LinkedIn access token using the refresh token."""
    if not user.linkedin_refresh_token:
        logging.error(f"No refresh token found for {user.email}")
        return None

    data = {
        "grant_type": "refresh_token",
        "refresh_token": user.linkedin_refresh_token,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }

    try:
        response = requests.post(TOKEN_URL, data=data)
        response.raise_for_status()
        token_data = response.json()
    except requests.RequestException as e:
        logging.error(f"Failed to refresh token for {user.email}: {e}")
        return None

    new_token = token_data.get("access_token")
    expires_in = token_data.get("expires_in", 0)

    if new_token:
        user.linkedin_access_token = new_token
        user.linkedin_expires_at = datetime.utcnow() + timedelta(seconds=expires_in)
        db.session.commit()
        return new_token
    return None

def get_valid_access_token(user):
    """Returns a valid LinkedIn access token, refreshing it if expired."""
    if user.linkedin_expires_at and user.linkedin_expires_at < datetime.utcnow():
        return refresh_linkedin_token(user)
    return user.linkedin_access_token

def post_to_linkedin(user, content):
    """Posts content to LinkedIn using a valid access token."""
    access_token = get_valid_access_token(user)

    if not access_token:
        logging.error("No valid LinkedIn token. Skipping post.")
        return False

    if not user.linkedin_id:  # Ensure LinkedIn ID is available
        logging.error("LinkedIn ID missing. Cannot post.")
        return False

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0",
    }

    data = {
        "author": f"urn:li:person:{user.linkedin_id}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": content},
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"  # Post visible PUBLIC or PRIVATE
        }
    }

    try:
        response = requests.post(POST_URL, json=data, headers=headers)
        response.raise_for_status()
        logging.info("Successfully posted to LinkedIn")
        return True

    except requests.RequestException as e:
        logging.error(f"Failed to post on LinkedIn: {e.response.status_code} - {e.response.text}")
        return False