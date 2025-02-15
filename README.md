# Linkedin-post-scheduler
Schedule for posting and provide your content and it will generate, send email to approve and post on approval.

SETUP AND INSTALLATION
1. Git clone the repository via url
2. Create a virtual environment with venv inside folder Project-gen
    python - m venv venv
3. Activate it:
    Windows:
        venv\Scripts\activate
    Mac/Linux:
        source venv/bin/activate
4. Install Dependencies
    pip install -r requirements.txt
5. Configure Environment Variables
    Inside Project-gen/backend/, there is an .env file kindly configure it first.
6. Set Up the Database
    Navigate to backend/:
        cd backend
    Initialize Alembic Migrations:
        flask db init
    * if you dont find a folder instance with database.db create one mannual now.
    Create Migration File:
        flask db migrate -m "Initial Migration"
    Apply Migrations:
        flask db upgrade
7. Run the Flask Application
    Ensure you're inside backend/:
        cd backend
        python app.py
The app will start running on http://127.0.0.1:5000/
