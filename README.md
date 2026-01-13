# 🔐 User Authentication System (Flask)

A secure and modern **User Authentication System** built using **Flask**, demonstrating real-world authentication workflows used in production applications.  
The project includes email verification, password reset, role-based access control, session management, and a professional UI with dark mode support.

---

## 📌 Features

### ✅ Authentication
- User Signup with email & password
- Secure Login & Logout
- Password hashing (Werkzeug)
- Session-based authentication using Flask-Login

### 📧 Email Workflows
- Email verification after signup (token-based)
- Forgot password & reset password via email link
- Secure time-limited tokens using `itsdangerous`

### 👥 Role-Based Access Control
- User roles:
  - **Admin**
  - **User**
- Restricted admin-only routes

### ⏱ Session Management
- Automatic logout after **15 minutes of inactivity**
- Session timeout works even if the browser tab remains open

### 🎨 UI & UX
- Modern, professional UI
- Gradient & glassmorphism design
- Dark mode toggle 🌙
- Show / Hide password 👁️
- Confirm password field
- Password strength indicator

---

## 🛠 Tech Stack

- **Backend:** Flask, Flask-Login, Flask-Mail
- **Database:** SQLite (SQLAlchemy ORM)
- **Frontend:** HTML, CSS, JavaScript
- **Security:** Password hashing, token-based verification
- **Environment Management:** python-dotenv

---

## 📁 Project Structure

User Authentication System/
│
├── app.py
├── models.py
├── utils.py
├── .env
├── instance/
│ └── database.db
│
├── templates/
│ ├── login.html
│ ├── signup.html
│ ├── forgot_password.html
│ ├── reset_password.html
│ ├── dashboard.html
│ └── admin.html
│
├── static/
│ ├── style.css
│ ├── password.js
│ ├── show_password.js
│ └── theme.js
│
├── venv/
└── README.md

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository
git clone <repository-url>
cd User-Authentication-System

2️⃣ Create Virtual Environment
python -m venv venv
venv\Scripts\activate   # Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Create .env File
SECRET_KEY=your_secret_key
MAIL_USERNAME=yourgmail@gmail.com
MAIL_PASSWORD=your_gmail_app_password
⚠️ Use Gmail App Password (not normal Gmail password)

5️⃣ Run the Application
python app.py
Open browser:
http://127.0.0.1:5000

🔐 Security Highlights
No plain-text passwords stored
Secure password hashing
Token-based email verification & reset
Role-based route protection
Session timeout handling
Environment variables for secrets

🧠 Authentication Flow
Signup → Email Verification → Login → Session → Auto Logout
🧪 Testing Notes
If email is not configured, user verification can be manually enabled in the database for testing.

Gmail SMTP requires 2-Step Verification + App Password.

📌 Future Enhancements
JWT-based authentication
OAuth (Google / GitHub login)
Rate limiting & brute-force protection
React frontend integration
Deployment on cloud (AWS / Render)

📄 License
This project is for educational purposes.