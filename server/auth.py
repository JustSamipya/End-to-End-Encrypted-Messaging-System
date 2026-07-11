import bcrypt
from cryptography.rsa_manager import *
 

class Auth:

    def __init__(self, database):
        self.database = database

    def hash_password(self, password):
        encoded_password = password.encode()
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(encoded_password,salt)
        hashed_password  = hashed_password.decode()
        return hashed_password

    def register(self, username, password):
        user = self.database.get_user(username)
        if user is not None:
             return False
        hashed_password = self.hash_password(password)
        private_key,public_key = generate_key_pair()
        save_private_key(username,private_key=private_key)
        self.database.register_user(username,hashed_password,public_key.decode())

        return True
    
    def register_with_public_key(self, username, password, public_key):
        user = self.database.get_user(username)
        if user is not None:
            return False
        hashed_password = self.hash_password(password)
        self.database.register_user(username, hashed_password, public_key)
        return True

    def login(self, username:str, password:str):
        user = self.database.get_user(username)
        if user is None:
            return False
        
        encoded_password = password.encode()
        stored_hash = user[2].encode() #hased password
        return bcrypt.checkpw(encoded_password,stored_hash)

        
