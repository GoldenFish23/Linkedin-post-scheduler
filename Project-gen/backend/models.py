from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    linkedin_id = db.Column(db.String(75), unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100),unique=True, nullable=False)
    topics = db.Column(db.Text, nullable=True)
    schedule = db.Column(db.String(100), nullable=True, default=None)
    linkedin_access_token = db.Column(db.String(500))  # Short-lived token
    linkedin_refresh_token = db.Column(db.String(500))  # Long-lived refresh token
    linkedin_expires_at = db.Column(db.DateTime)

    def __init__(self, linkedin_id, first_name, last_name, email):
        self.linkedin_id = linkedin_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email