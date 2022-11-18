import sqlite3

class DataBase:
    def __init__(self,db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        
    def user_exists(self,user_tg_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM users WHERE user_tg_id = ?", (user_tg_id,)).fetchmany(1)
            return bool(len(result))
        
    def add_user(self,user_tg_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO 'users' ('user_tg_id') VALUES (?)", (user_tg_id,))
    
    def get_users(self):
        with self.connection:
            return self.cursor.execute("SELECT 'user_id' FROM 'users'").fetchall()