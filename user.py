import sqlite3
from flask_login import LoginManager, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

#user object
class User(UserMixin):
#initialize club object with its parameters
    #future parameters: google classroom code(?)
    def __init__(self, id, first_name, last_name, email, password_hash):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email 
        # self.email_verification_token = ""
        self.password_hash = password_hash
        # self.is_verified = False
        # self.is_admin = False
def set_password(password):
        password_hash = generate_password_hash(password)
        return password_hash
def check_password(self, password):
        return check_password_hash(self.password_hash, password)

def register_user(User):
    db = sqlite3.connect('db/database.db')
    db_cursor = db.cursor()
    db_cursor.execute(
                """INSERT INTO users
                (first_name, last_name, email, password_hash) VALUES (?,?,?,?)""",
                (User.first_name, User.last_name, User.email, User.password_hash)
            )
    db.commit()
    db.close()

def search_user(email):
    db = sqlite3.connect('db/database.db')
    db_cursor = db.cursor()
    db_cursor.execute(
            #have to add the other parameters later
                """SELECT * FROM users
                WHERE email=?""",
                (email,)
            )
    data = db_cursor.fetchall()
    db.close()
    if not data:
        return False
    return True
# Generate a Verification Token:
def generate_verification_token():
    return secrets.token_urlsafe(50)  # Adjust the token length as needed
