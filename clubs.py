import sqlite3
import csv
import os
#create the club class just for some parity with sqlalchemy. Will serve useful when creating a club.
class Club():
    #initialize club object with its parameters
    #future parameters: google classroom code(?)
    def __init__(self, id, faculty_name, club_name, club_description, meeting_location, meeting_days):
        self.id = id
        self.faculty_name = faculty_name
        self.club_name = club_name
        self.club_description = club_description
        self.meeting_location = meeting_location
        self.meeting_days = meeting_days
#csv parsing functions
def parse_csv_data(csv_file):
    reader = csv.reader(csv_file)
    headers = next(reader)
    data = [row for row in reader]
    # print(data)
    return data
def add_csv_data_to_database(file):
    csv_data = parse_csv_data(file)
    db = sqlite3.connect('db/database.db')
    db_cursor = db.cursor()
    for club in csv_data:
        try:
            new_club = Club(None, club[0], club[1], club[2], club[3], club[4])
            # print(new_club.faculty_name)
            
            db_cursor.execute(
                """INSERT INTO clubs
                (faculty_name, club_name, club_description, meeting_location, meeting_days) VALUES (?,?,?,?,?)""",
                (new_club.faculty_name, new_club.club_name, new_club.club_description, new_club.meeting_location, new_club.meeting_days)
            )
            db.commit()
        except Exception as e:
            db.rollback()
    db.close()

#create my clubs class for the clubs the user adds
class My_Clubs():
    def __init__(self, id, user_id, clubs_id):
        self.id = id
        self.user_id = user_id
        self.clubs_id = clubs_id
      

#initialize official clubs using club list from official 2324 club list
def initialize_clubs():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    csv_file_path = os.path.join(current_directory, 'init', '2324ClubList.csv')
    with open(csv_file_path, 'r') as file:
        add_csv_data_to_database(file)

#get all clubs by a sql query
def get_all_clubs():
    #db intialization
    db = sqlite3.connect('db/database.db')
    db_cursor = db.cursor()
    #get all clubs
    db_cursor.execute("SELECT * FROM clubs")
    data = db_cursor.fetchall()
    db.close()
    return data

#search for club by name
def search_clubs(name):
    #db intialization
    db = sqlite3.connect('db/database.db')
    db_cursor = db.cursor() 
    #prepared statement to prevent sql injection    
    db_cursor.execute("SELECT * FROM clubs WHERE club_name LIKE ?", (name,))
    data = db_cursor.fetchall()
    db.close()
    return data

def search_club_by_id(id):  
    #db intialization
    db = sqlite3.connect('db/database.db')
    db_cursor = db.cursor() 
    #prepared statement to prevent sql injection    
    db_cursor.execute("SELECT * FROM clubs WHERE id = ?", (id,))
    data = db_cursor.fetchall()
    db.close()
    return data

##### USER CLUB STUFF
#need to pass user parameters of user id, club id, and later on if there is edit functionality?
def add_club_to_user(user_id, club_id):
    print(user_id, club_id)
    db = sqlite3.connect('db/database.db')
    db_cursor = db.cursor()
    #add to the my_clubs table
    try: 
        db_cursor.execute(
                    """INSERT INTO my_clubs
                    (user_id, club_id) VALUES (?,?)""",
                    (user_id, club_id)
        )
        db.commit()
    except Exception as e:
        db.rollback()
    db.close()

def user_club_exists(user_id, club_id):
    db = sqlite3.connect('db/database.db')
    db_cursor = db.cursor()
    #search for my_clubs where user_id is the user_id specified
    db_cursor.execute("SELECT * FROM my_clubs WHERE user_id = ? AND club_id = ?", (user_id, club_id,))
    data = db_cursor.fetchall()
    db.close()
    return data 

def get_user_clubs(user_id):
    db = sqlite3.connect('db/database.db')
    db_cursor = db.cursor()
    #search for my_clubs where user_id is the user_id specified
    db_cursor.execute("SELECT * FROM my_clubs WHERE user_id = ?", (user_id,))
    data = db_cursor.fetchall()
    db.close()
    return data