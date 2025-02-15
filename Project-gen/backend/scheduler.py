import logging
from apscheduler.schedulers.background import BackgroundScheduler
from models import User
from linkedin import refresh_linkedin_token
from email_service import send_approval_email
from creation import generate_content
from datetime import datetime
from flask import Flask
from models import db

scheduler = BackgroundScheduler()

def daily_task(app: Flask):
    """Fetch users scheduled for today and send content approval emails."""
    # from app import app
    with app.app_context():
        today = datetime.today().strftime("%a")  # Get current weekday (Mon, Tue, etc.)
        
        users = db.session.query(User).filter(User.schedule.like(f"%{today}%")).all()  # Fetch users with today's schedule
        
        for user in users:
            content = generate_content(user)
            send_approval_email(user, content)

def refresh_tokens(app: Flask):
    """Refresh LinkedIn tokens for users whose tokens have expired."""
    with app.app_context():
        expired_users = db.session.query(User).filter(User.linkedin_expires_at < datetime.utcnow()).all()  # Find users whose access token is expired.
        
        for user in expired_users:
            refresh_linkedin_token(user)

def start_scheduler(app: Flask):
    """Start the scheduler with periodic tasks."""
    if not scheduler.running:  # Check if scheduler is already running
        scheduler.add_job(daily_task, "interval", minutes=3, args=[app])
        scheduler.add_job(refresh_tokens, "interval", hours=1, args=[app])
        scheduler.start()
        logging.info("Scheduler started successfully.")
    else:
        logging.info("Scheduler is already running.")