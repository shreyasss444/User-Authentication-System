from itsdangerous import URLSafeTimedSerializer
from flask import current_app

def generate_token(email):
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    return serializer.dumps(email, salt="auth-token")

def verify_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    return serializer.loads(token, salt="auth-token", max_age=expiration)
