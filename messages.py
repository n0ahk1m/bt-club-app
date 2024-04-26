import sqlite3
class Message():
    def __init__(self, id, user_id, club_id, message_content, message_date):
        self.id = id
        self.user_id = user_id
        self.club_id = club_id
        self.message_content = message_content
        self.message_date = message_date
#get all messages by club id 
def get_messages(club_id):
    db = sqlite3.connect('db/database.db')
    db_cursor = db.cursor()
    #get all messages by the club_id 
    db_cursor.execute("SELECT * FROM messages WHERE club_id = ?", (club_id,))
    data = db_cursor.fetchall()
    db.close()
    return data
#OWNERS OF THE CLUB ONLY!
def post_message(user_id, club_id, message_content, message_date):
    db = sqlite3.connect('db/database.db')
    db_cursor = db.cursor()

    new_message = Message(None, user_id, club_id, message_content, message_date)

    try: 
        db_cursor.execute(
            """INSERT INTO messages
            (message_content, message_date, user_id, club_id) VALUES (?,?,?,?)""",
            (new_message.message_content, new_message.message_date, new_message.user_id, new_message.club_id,)
        )
        db.commit()
        print('successful!')
    except Exception as e:
        db.rollback()
        
#LATER UNABLE TO EDIT ADMIN OR TEACHER MESSAGES
def edit_message(message_id, new_message):
    db = sqlite3.connect('db/database.db')
    db_cursor = db.cursor()
    try:
            
        db_cursor.execute(
            """UPDATE messages SET
            (message_content, message_date, user_id, club_id) SET message_content = ? WHERE id = ?""",
            (new_message.message_content, new_message.message_date, new_message.user_id, new_message.club_id)
        )
        db.commit()
    except Exception as e:
        db.rollback()
    
