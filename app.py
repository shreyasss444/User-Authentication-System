import os
from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_mail import Mail, Message
from datetime import timedelta

from models import db, User
from utils import generate_token, verify_token

app = Flask(__name__)

# ---------------- CONFIG ----------------
app.config["SECRET_KEY"] = "super-secret-key"
db_path = os.path.join(app.instance_path, "database.db")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_path
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=15)

# Email config
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "your_email@gmail.com"
app.config["MAIL_PASSWORD"] = "your_app_password"

# ---------------- INIT ----------------
db.init_app(app)
mail = Mail(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ---------------- SESSION TIMEOUT ----------------
@app.before_request
def session_timeout():
    session.permanent = True

# ---------------- ROUTES ----------------

@app.route("/")
def home():
    return redirect(url_for("login"))

# -------- SIGNUP --------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        if User.query.filter_by(email=email).first():
            flash("Email already exists")
            return redirect(url_for("signup"))

        user = User(email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        token = generate_token(email)
        verify_link = url_for("verify_email", token=token, _external=True)

        msg = Message(
            "Verify Your Email",
            sender=app.config["MAIL_USERNAME"],
            recipients=[email]
        )
        msg.body = f"Click to verify your account:\n\n{verify_link}"
        mail.send(msg)

        flash("Check your email to verify your account")
        return redirect(url_for("login"))

    return render_template("signup.html")

# -------- EMAIL VERIFY --------
@app.route("/verify/<token>")
def verify_email(token):
    try:
        email = verify_token(token)
        user = User.query.filter_by(email=email).first()
        user.is_verified = True
        db.session.commit()
        flash("Email verified successfully")
    except:
        flash("Invalid or expired verification link")

    return redirect(url_for("login"))

# -------- LOGIN --------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            flash("Invalid credentials")
            return redirect(url_for("login"))

        if not user.is_verified:
            flash("Please verify your email first")
            return redirect(url_for("login"))

        login_user(user)
        return redirect(url_for("dashboard"))

    return render_template("login.html")

# -------- DASHBOARD --------
@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

# -------- ADMIN --------
@app.route("/admin")
@login_required
def admin():
    if current_user.role != "admin":
        return "Access Denied", 403
    return render_template("admin.html")

# -------- LOGOUT --------
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully")
    return redirect(url_for("login"))

# -------- FORGOT PASSWORD --------
@app.route("/forgot", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form["email"]
        user = User.query.filter_by(email=email).first()

        if user:
            token = generate_token(email)
            reset_link = url_for("reset_password", token=token, _external=True)

            msg = Message(
                "Password Reset",
                sender=app.config["MAIL_USERNAME"],
                recipients=[email]
            )
            msg.body = f"Reset your password using this link:\n\n{reset_link}"
            mail.send(msg)

        flash("If the email exists, a reset link has been sent")
        return redirect(url_for("login"))

    return render_template("forgot_password.html")

# -------- RESET PASSWORD --------
@app.route("/reset/<token>", methods=["GET", "POST"])
def reset_password(token):
    try:
        email = verify_token(token)
    except:
        flash("Invalid or expired reset link")
        return redirect(url_for("login"))

    if request.method == "POST":
        password = request.form["password"]
        user = User.query.filter_by(email=email).first()
        user.set_password(password)
        db.session.commit()

        flash("Password updated successfully")
        return redirect(url_for("login"))

    return render_template("reset_password.html")

# ---------------- RUN ----------------
if __name__ == "__main__":
    if not os.path.exists(app.instance_path):
        os.makedirs(app.instance_path)

    with app.app_context():
        db.create_all()

    app.run(debug=True)