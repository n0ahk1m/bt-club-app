from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import os, io
from sqlalchemy import desc, asc
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from flask_login import LoginManager, UserMixin
from flask_mail import Mail
from flask_mail import Message
#import app file will bring other imports in
from __main__ import app

#set up login database
login_manager = LoginManager(app)
login_manager.login_view = 'login' #specify the login route
login_manager.login_message = "Unauthorized access please log in!"
login_manager.login_message_category = 'danger'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = 'emregemici@gmail.com'
# Consider using app secrets or environment variables
app.config['MAIL_PASSWORD'] = 'cxke ztxi bhac vqim'  
# Set the default sender
app.config['MAIL_DEFAULT_SENDER'] = 'emregemici@gmail.com'
mail = Mail(app)

db = SQLAlchemy(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    is_teacher = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Generate a Verification Token:
def generate_verification_token():
    return secrets.token_urlsafe(50)  # Adjust the token length as needed

# Send a Verification Email:
def send_verification_email(user):
    verification_link = (
        f"http://127.0.0.1:5000/verify_email/{user.email_verification_token}"
    )
    msg = Message("Verify Your Email", recipients=[user.email])
    msg.body = f"Click the following link to verify your email: {verification_link}"
    mail.send(msg)
