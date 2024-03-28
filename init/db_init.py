import sqlite3

def create_tables():
    db_master = sqlite3.connect('db/database.db')
    db = db_master.cursor()
    #just to make sure initalization does not get appended rather than a new thing being created
    db.execute("DROP TABLE IF EXISTS clubs")
    db_master.commit()
    #the queries to create the user and clubs table
    '''is_verified BOOLEAN DEFAULT FALSE,
        email_verification VARCHAR(255),
        is_admin BOOLEAN DEFAULT FALSE'''
    creation_queries = [
        """CREATE TABLE IF NOT EXISTS users (
           id INTEGER PRIMARY KEY,
           first_name VARCHAR(255) NOT NULL,
           last_name VARCHAR(255) NOT NULL,
           email VARCHAR UNIQUE,
           password_hash VARCHAR(255)
           
           ) """,
        """CREATE TABLE IF NOT EXISTS clubs (
            id INTEGER PRIMARY KEY,
            faculty_name VARCHAR(50),
            club_name VARCHAR(50) UNIQUE,
            club_description TEXT,
            meeting_location VARCHAR(50),
            meeting_days VARCHAR(50)
        )
        """,
    ]
    for create_query in creation_queries:
        db.execute(create_query)
    db_master.commit()
    db.close()
    db_master.close()
def create_admin():
    pass