from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_oauthlib.client import OAuth
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
from clubs import *
import os

app = Flask(__name__)
app.secret_key = os.urandom(12)

oauth = OAuth(app)
#set mail 
mail = Mail(app)
#main page

#login manager
login_manager = LoginManager(app)
login_manager.login_view = 'login' #specify the login route
login_manager.login_message = "Unauthorized access please log in!"
login_manager.login_message_category = 'danger'

@app.route('/')
def home():
    return render_template("home.html")
@login_manager.user_loader
def load_user(user_id):
    #just run the load user connection here
    conn = sqlite3.connect('db/database.db')
    curs = conn.cursor()
    curs.execute("SELECT * from users where id = (?)",[user_id])
    lu = curs.fetchone()
    if lu is None:
        return None
    else:
        return User(int(lu[0]), lu[1], lu[2], lu[3], lu[4])
    
@app.route('/login', methods=['GET','POST'])
def login():
    GOOGLE_CLIENT_ID = '954980088912-ukn276fifnqm5g5fncnptb9pnl3esmhs.apps.googleusercontent.com'
    GOOGLE_CLIENT_SECRET = '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'

    CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
    oauth.register(
        name='google',
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        server_metadata_url=CONF_URL,
        client_kwargs={
            'scope': 'openid email profile'
        }
    )

    # Redirect to google_auth function
    redirect_uri = url_for('google_auth', _external=True)
    print(redirect_uri)
    return oauth.google.authorize_redirect(redirect_uri)

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        #replace query using sqlite3 instead of alchemy here ------------------------------------------
        user = search_user(email)
        print(user[0][3])
        if user and check_password(user[0][4], password):
            print(user[0][0])
            User = load_user(user[0][0])
            login_user(User)
            print(User)
            #get the id of the user and use it as a session token variable
            session['user_id'] = user[0]
            flash("Logged in successfully!", "success")
            return redirect(url_for('home'))
        else:
            flash("Invalid credentials!","danger")
        return render_template("login.html")
    return render_template("login.html")

@app.route('/authorized')
def authorized():
    token = oauth.google.authorize_access_token()
    user = oauth.google.parse_id_token(token,None)
    google_user = User.query.filter_by(email=user.email).first()

    # add new user to database
    if not google_user:
        google_user = User(email=user.email,name=user.given_name,lastname=user.family_name, picture=user.picture,admin=user.email in admins)
        db.session.add(google_user)
        db.session.commit()
        print('new google user added')
    else:
        print('google user exist')
    login_user(google_user)
    # if the above check passes, then we know the user has the right credentials  
    return redirect('/register')

@app.route('/profile', methods=['GET','POST'])
def profile():
    return render_template('profile.html')

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
        if user:
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
    initialize_clubs()
    app.secret_key = "super_secret_key"  # Change this to a secure ENCRYPTED key
    app.run(debug=True)