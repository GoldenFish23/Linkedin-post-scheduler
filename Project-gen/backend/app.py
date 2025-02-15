import os, cohere
from flask import Flask, redirect, request, session, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from linkedin import linkedin_bp, post_to_linkedin
from datetime import datetime
from models import db, User
from flask_mail import Mail, Message
from email_service import send_approval_email
from creation import generate_content

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Database & Security Configurations
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
co = cohere.Client(os.getenv("AI_API_KEY"))

# Initialize Database & Migrations
mail = Mail(app)
db.init_app(app)
migrate = Migrate(app, db)

# Register Blueprints
app.register_blueprint(linkedin_bp)

# Import and Start the Scheduler after initializing the app
from scheduler import start_scheduler

@app.route("/")
def home():
    return "<h2>LinkedIn OAuth with Free Scopes</h2><p><a href='/login'>Login with LinkedIn</a></p>"

@app.route("/dashboard", methods=["GET"])
def dashboard():
    if "user_id" not in session:
        return redirect('/login')
    
    user = db.session.get(User, session["user_id"])
    return render_template("dashboard.html", user=user)

@app.route("/update_dashboard", methods=['POST'])
def update_dashboard():
    if "user_id" not in session:
        return redirect('/login')
    
    user = db.session.get(User, session["user_id"])
    user.topics = request.form.get("topics")
    selected_days = request.form.getlist("schedule")
    user.schedule = ",".join(selected_days)

    db.session.commit()
    return redirect("/dashboard")

@app.route("/approve/<int:user_id>")
def approve_post(user_id):
    user = db.session.get(User, user_id)
    if user:
        content = generate_content(user)  # Regenerate the content if needed
        post_to_linkedin(user, content)  # Post the content to LinkedIn
        return "Post approved and published successfully!", 200
    return "User not found", 404

@app.route("/admin")
def admin():
    users = User.query.all()
    return render_template("admin.html", users=users)

""" Testing AI Integration """
# @app.route("/test_ai")
# def test_openai():
#     co = cohere.Client(os.getenv("AI_API_KEY"))
#     try:
#         response = co.generate(
#             model="command-r-plus",
#             prompt="Write a short article about AI",
#             max_tokens=200
#         )
#         return jsonify({"text": response.generations[0].text})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
    
""" Testing Mail Integration """
# @app.route('/test_mail')
# def send_test_mail():
#     try:
#         msg = Message(
#             subject="Test Email from Flask",
#             sender=app.config['MAIL_USERNAME'],
#             recipients=["example@mail.com"],  # Replace with your recipient email
#             body="This is a test email to check if mail sending is working in Flask."
#         )
#         mail.send(msg)
#         return jsonify({"message": "Test email sent successfully!"})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":  # Prevent scheduler from running twice
        with app.app_context():
            start_scheduler(app)
    app.run(debug=False)
