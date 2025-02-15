from flask_mail import Mail, Message
from dotenv import load_dotenv
import os
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Run Mail service
mail = Mail()

def send_approval_email(user, content):
    """
    Sends an approval email to the user with their LinkedIn post content.
    """
    try:
        approval_link = f"http://127.0.0.1:5000/approve/{user.id}"
        msg = Message(
            'Approval Request',
            sender=os.getenv('MAIL_USERNAME'),
            recipients=[user.email]
        )
        msg.html = f"""
            <html>
            <body>
                <p>Hello {user.first_name},</p>
                <p>Here’s your LinkedIn post for today:</p>
                <blockquote style="background: #f4f4f4; padding: 10px; border-left: 5px solid #007bff;">
                    {content}
                </blockquote>
                <p>Click the button below to approve and post it:</p>
                <a href="{approval_link}" style="
                    background-color: #007bff; 
                    color: white; 
                    padding: 10px 15px; 
                    text-decoration: none; 
                    border-radius: 5px;
                    font-weight: bold;
                ">
                    Approve & Post
                </a>
                <p>If you did not request this, you can ignore this email.</p>
            </body>
            </html>
            """
        """Use some try-error statement here"""
        mail.send(msg)
        logging.info(f"Approval email sent to {user.email}")
        return f"Email sent to {user.email}"
    
    except Exception as e:
        logging.error(f"Failed to send email to {user.email}: {str(e)}")
        return f"Error sending email to {user.email}: {str(e)}"