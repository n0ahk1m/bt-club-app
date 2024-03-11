import sqlite3
from flask_login import LoginManager, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
#user object
class User(UserMixin):
#initialize club object with its parameters
    #future parameters: google classroom code(?)
    def __init__(self, id, first_name, last_name, email, password_hash, email_verification_token, is_verified):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email 
        self.password_hash = password_hash
        self.email_verification_token = email_verification_token
        self.is_verified = is_verified
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

def register_user():
    pass
