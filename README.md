# LINKEDIN POST SCHEDULER 🚀
*A Flask-based LinkedIn automation tool with AI-generated content, email approvals, and scheduled posting.<br>*

This application automates daily LinkedIn content posting using Flask and Cohere AI. It allows users to:<br>
✅ Schedule posts based on their chosen days<br>
✅ Generate AI-powered content using Cohere<br>
✅ Receive an approval email before posting<br>
✅ Post content automatically on approval<br>

## 📌 FEATURES<br>
🕒 Automated LinkedIn Posting<br>
📅 Custom Scheduling for Posts<br>
🤖 AI-Powered Content Generation (via Cohere AI)<br>
📧 Email Approval Before Posting<br>
🔗 Seamless LinkedIn API Integration<br>

## 🔧 SETUP AND INSTALLATION
#### 1. Git clone the repository via repository url.
#### 2. Create a virtual environment with venv inside folder Project-gen.<br>
*&emsp; python - m venv venv</p>*
#### 3. Activate it:
- Windows:<br>
*&emsp; venv\Scripts\activate*
- Mac/Linux:<br>
*&emsp; source venv/bin/activate*
#### 4. Install the Required Dependencies.<br>
*&emsp; pip install -r requirements.txt*
#### 5. Configure Environment Variables.<br>
&emsp; Inside Project-gen/backend/, there is an .env file kindly configure it first.
#### 6. Set Up the Database<br>
- Navigate to backend/:<br>
*&emsp; cd backend<br>*
- Initialize Alembic Migrations:<br>
*&emsp; flask db init<br>*
&emsp; * if you dont find a folder instance with database.db create one mannual now.<br>
- Create Migration File:<br>
*&emsp; flask db migrate -m "Initial Migration"<br>*
- Apply Migrations:<br>
*&emsp; flask db upgrade<br>*
#### 7. Run the Flask Application
- Ensure you're inside backend/:<br>
*&emsp; cd backend<br>*
*&emsp; python app.py<br>*
The app will start running on http://127.0.0.1:5000/

## 🔥 USAGE GUIDE
1. Login via LinkedIn
2. Visit http://127.0.0.1:5000/
3. Click "Login with LinkedIn"
4. Authenticate & get redirected to the dashboard
5. Update Topics & Schedule
6. Navigate to /dashboard
7. Update Topics & Days for Scheduling
8. Click Save
9. Approve & Publish LinkedIn Posts
10. You’ll receive an approval email with a button
11. Click Approve to post automatically on LinkedIn
