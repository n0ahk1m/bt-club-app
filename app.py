from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from werkzeug.utils import secure_filename
import csv
from datetime import datetime
from flask_mail import Mail
from flask_mail import Message
from flask_login import LoginManager, UserMixin
from flask_login import login_user, current_user, logout_user, login_required
import random
import base64
from cryptography.fernet import Fernet
#external py modules
from init.db_init import create_tables
from user import *
# from clubs import *

app = Flask(__name__)
#set mail 
mail = Mail(app)
#main page
@app.route('/')
def home():
    return render_template("home.html")

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        #replace query using sqlite3 instead of alchemy here ------------------------------------------
        session['user_id'] =user.id
        if user and user.check_password(password):
            login_user(user)
            flash("Logged in successfully!", "success")
            return redirect(url_for('index'))
        else:
            flash("Invalid credentials!","danger")
        return render_template("login.html")
    return render_template("login.html")

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == "POST":
        # Get form data
        name = request.form.get("name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        # image_file = request.files.get("image")
        # is_mfa_enabled = request.form.get("mfa")
        # phoneNumber = request.form.get("phoneNumber")

        # Validate form data (add your own validation logic)
        if not (
            name
            and last_name
            and email
            and password
            and confirm_password
            # and image_file
            # and accept_terms
        ):
            
        # Handle invalid input
            flash("Please fill in all fields.", "danger")
            return render_template("register.html")
        
        #handle if existing user
        # user = User.query.filter_by(email=email).first()
        user = search_user(email)
        print(user)

        if user == False:
            flash("User already exist! Try a different email", "danger")
            return render_template("register.html")
        if password != confirm_password:
            # Handle password mismatch
            flash("Passwords do not match.", "danger")
            return render_template("register.html")

        # Get image data
        # image_data = image_file.read()

        # Create a new user instance
        new_user = User(None, name, last_name, email, set_password(password))
            # image_data=image_data,
            # email_verification_token=generate_verification_token(),
            # is_mfa_enabled= True if is_mfa_enabled else False,
            # phoneNumber = phoneNumber
        register_user(new_user)
        flash("Account created successfully! Please check your email to verify.", "success")
        return redirect(url_for('login'))
    return render_template("register.html")

# Send a Verification Email:
# def send_verification_email(user):
#     verification_link = (
#         f"http://127.0.0.1:5000/verify_email/{user.email_verification_token}"
#     )
#     msg = Message("Verify Your Email", recipients=[user.email])
#     msg.body = f"Click the following link to verify your email: {verification_link}"
#     mail.send(msg)


@app.route('/clubs', methods=['GET', 'POST'])
def clubs():
    if request.method=='GET':
        all_clubs = get_all_clubs()
        return render_template("clubs.html", clubs=all_clubs)

@app.route('/my_clubs', methods=['GET', 'POST'])
def myclubs():
    if request.method == 'GET':
        return render_template("my_clubs.html")

@app.route('/calendar')
def calendar():
    return render_template("calendar.html")

if __name__ == "__main__":
    #create the tables
    create_tables()
    #create the clubs list
    # initialize_clubs()
    app.secret_key = "super_secret_key"  # Change this to a secure ENCRYPTED key
    app.run(debug=True)