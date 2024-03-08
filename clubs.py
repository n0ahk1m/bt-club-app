import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, asc
import csv


db = SQLAlchemy(app)



class Clubs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    faculty = db.Column(db.String(50))
    description = db.Column(db.String(50))
    location = db.Column(db.String(50))
    meeting_day = db.Column(db.String(50))

#create a club
def create_club():
    pass
