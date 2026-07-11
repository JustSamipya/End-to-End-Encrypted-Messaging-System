from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import os


def generate_key_pair():
    key = RSA.generate(2048)

    private_key = key.export_key()

    public_key = key.publickey().export_key()

    return private_key, public_key

def save_private_key(username, private_key):
    os.makedirs("keys",exist_ok=True)

    filename = f"keys/{username}_private.pem"

    with open(filename, "wb") as file:
        file.write(private_key)



def load_private_key(username):
    filename = f"keys/{username}_private.pem"

    with open(filename, "rb") as file:
        return RSA.import_key(file.read())
    
def encrypt_aes_key(aes_key,public_key):
    rsa_key = RSA.import_key(public_key)

    cipher = PKCS1_OAEP.new(rsa_key)

    encrypted_key = cipher.encrypt(aes_key)

    return encrypted_key


def decrypt_aes_key(encrypted_key, private_key):

    cipher = PKCS1_OAEP.new(private_key)

    aes_key = cipher.decrypt(encrypted_key)

    return aes_key