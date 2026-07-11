from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def generate_aes_key():
    return get_random_bytes(32)

def encrypt_message(message,aes_key):
    cipher = AES.new(aes_key,AES.MODE_EAX)
    cipher_text,tag = cipher.encrypt_and_digest(message.encode())

    return cipher.nonce,tag,cipher_text

def decrypt_message(nonce, tag, ciphertext, aes_key):

    cipher = AES.new(
        aes_key,
        AES.MODE_EAX,
        nonce=nonce
    )

    plaintext = cipher.decrypt_and_verify(
        ciphertext,
        tag
    )

    return plaintext.decode()