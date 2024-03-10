from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from werkzeug.utils import secure_filename
import csv
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from flask_mail import Mail
from flask_mail import Message
from flask_login import LoginManager, UserMixin
from flask_login import login_user, current_user, logout_user, login_required
import random
import base64
from cryptography.fernet import Fernet
#external py modules
from init.db_init import create_tables
# import user
from clubs import *

app = Flask(__name__)
#main page
@app.route('/')
def home():
    return render_template("home.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/register', methods=['GET','POST'])
def register():
    return render_template("register.html")

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
    app.secret_key = ""  # Change this to a secure ENCRYPTED key
    app.run(debug=True)