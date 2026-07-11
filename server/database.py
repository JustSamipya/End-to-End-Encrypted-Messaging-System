import sqlite3



class Database:

    def __init__(self):
        self.database_name = "chat.db"

    def create_tables(self):
        conn =sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute(""" CREATE TABLE IF NOT EXISTS users(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password_hash TEXT NOT NULL,
                    public_key TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP) 
                    """)
        
        cursor.execute(""" CREATE TABLE IF NOT EXISTS messages(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        sender TEXT NOT NULL,
                        receiver TEXT NOT NULL,
                        sender_encrypted_key TEXT  NOT NULL,
                        receiver_encrypted_key TEXT NOT NULL,
                        nonce TEXT NOT NULL,
                        tag TEXT NOT NULL,
                        ciphertext TEXT NOT NULL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)
                        """)
        conn.commit()
        conn.close()

    def register_user(self,username,password_hash,public_key):
        conn =sqlite3.connect(self.database_name)
        cursor = conn.cursor()

        cursor.execute(
            """ INSERT INTO users(username,password_hash,public_key)
            VALUES(?,?,?) 
            """,
            (username,password_hash,public_key)
        )
        conn.commit()
        conn.close()

    def get_user(self,username):
        conn =sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username= ?',(username,))
        
        data = cursor.fetchone()
        conn.close()
        return data
    
    def save_message(self,sender,receiver,sender_encrypted_key,receiver_encrypted_key,nonce,tag,ciphertext):
        print(f"Saving message: {sender} -> {receiver}")
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO messages (sender,receiver,sender_encrypted_key,receiver_encrypted_key,nonce,tag,ciphertext
            )
            VALUES (?, ?, ?, ?, ?,?,?)
            """,
            (sender,receiver,sender_encrypted_key,receiver_encrypted_key,nonce,tag,ciphertext)
            
        )

        conn.commit()
        conn.close()
    def load_messages(self, user1, user2):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT sender, receiver,sender_encrypted_key,receiver_encrypted_key,nonce,tag, ciphertext, timestamp FROM messages
            WHERE
                (sender = ? AND receiver = ?)
                OR
                (sender = ? AND receiver = ?)
            ORDER BY timestamp ASC
            """,
            (
                user1,
                user2,
                user2,
                user1
            )
        )

        messages = cursor.fetchall()

        conn.close()

        return messages
    
    def get_public_key(self,username):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()

        cursor.execute(""" SELECT public_key FROM users
                       WHERE username = ? """,
                       (username,)
                       )
        row = cursor.fetchone()

        conn.close()

        if row is None:
            return None

        return row[0]
            
         


        
    








