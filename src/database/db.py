import sqlite3

class Database():
    
    def __init__(self, db_file):
        self.connection= sqlite3.connect(db_file)
        self.cursor= self.connection.cursor()
        
    def add_user(self, user_id, username, full_name):
        with self.connection:
            self.cursor.execute("INSERT INTO users (user_id, username, full_name) VALUES (?, ?, ?)", (user_id, username, full_name, ))
            
    def get_user(self, user_id=None):
        with self.connection:
            if user_id:
                return self.cursor.execute("SELECT * FROM users WHERE user_id= ?", (user_id, )).fetchone()
            else:
                return self.cursor.execute("SELECT * FROM users").fetchall()            

    def up_username(self, user_id, username, full_name):
        with self.connection:
            self.cursor.execute("UPDATE users SET username= ?, full_name=? WHERE user_id= ?", (username, full_name, user_id, ))
            
    def user_bal(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT balance FROM users WHERE user_id=?", (user_id, )).fetchone()[0]
        
    def get_games(self, result=None):
        with self.connection:
            if result:
                return self.cursor.execute("SELECT * FROM auctions").fetchall()
            else:
                return self.cursor.execute("SELECT name, bet FROM auctions").fetchall()
        
    def add_auction(self, data):
        with self.connection:
            self.cursor.execute("INSERT INTO auctions (user_id, name, bet, date, end_date) VALUES (?, ?, ?, ?, ?)", 
                                (data.get('user_id'),
                                 data.get('name'),
                                 data.get('bet'),
                                 data.get('date'),
                                 data.get('end_date'),))
            
            self.cursor.execute(f"""CREATE TABLE a{data.get('name')} (
                                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                                user_id INTEGER,
                                bet     INTEGER,
                                date    INTEGER)""")
            
            self.cursor.execute(f"INSERT INTO a{data.get('name')} (user_id, bet, date) VALUES (?, ?, ?)", 
                                (data.get('user_id'),
                                 data.get('bet'),
                                 data.get('date'),))
            
    def up_balance(self, user_id, sum):
        with self.connection:
            self.cursor.execute("UPDATE users SET balance= balance + ? WHERE user_id= ?", (sum, user_id, ))
        
    def get_game_Byid(self, au_id):
        with self.connection:
            return self.cursor.execute("SELECT * FROM auctions WHERE name= ?", (au_id, )).fetchone()
        
    def count_users(self, au_id):
        with self.connection:
            return self.cursor.execute(f"SELECT COUNT(id) FROM a{au_id}").fetchone()[0]
        
    def last_bet(self, au_id):
        with self.connection:
            return self.cursor.execute(f"SELECT * FROM a{au_id} WHERE id in (SELECT MAX(id) FROM a{au_id})").fetchone()
        
    def new_bet(self, data):
        with self.connection:
            self.cursor.execute(f"INSERT INTO a{data.get('name')} (user_id, bet, date) VALUES (?, ?, ?)", 
                                (data.get('user_id'),
                                 data.get('bet'),
                                 data.get('date'),))
            
            self.cursor.execute(f"UPDATE auctions SET end_date= ?, bet=bet+? WHERE name= ?", (data.get('date')+900, data.get('bet'), data.get('name'),))
            
    def delete_auction(self, au_id):
        with self.connection:
            self.cursor.execute(f"DELETE FROM auctions WHERE name= ?", (au_id, ))
            self.cursor.execute(f"DROP TABLE a{au_id}")
            
    def get_desc(self):
        with self.connection:
            return self.cursor.execute("SELECT * FROM descrip").fetchall()
        
    def add_desc(self, au_id, type= False):
        with self.connection:
            if type:
                self.cursor.execute("INSERT INTO descrip (auction_id, type) VALUES (?, ?)", (au_id, type, ))
            else:
                self.cursor.execute("INSERT INTO descrip (auction_id) VALUES (?)", (au_id, ))
        
    def del_desc(self, id_):
        with self.connection:
            self.cursor.execute("DELETE FROM descrip WHERE id= ?", (id_,))
        
    def get_allbets(self, au_id, user_id=None):
        with self.connection:
            if user_id:
                return self.cursor.execute(f"SELECT * FROM a{au_id} WHERE user_id != ? GROUP BY user_id", (user_id,)).fetchall()
            else:
                return self.cursor.execute(f"SELECT * FROM a{au_id} GROUP BY user_id").fetchall()