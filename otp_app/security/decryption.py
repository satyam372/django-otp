import base64
from Crypto.Cipher import AES
from base64 import b64decode
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

def decrypt_data(encrypted_data_base64, secret_key_base64, iv_base64):

    key = b64decode(secret_key_base64)
    iv = b64decode(iv_base64)
    encrypted_data = b64decode(encrypted_data_base64)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = cipher.decrypt(encrypted_data)

    try:
        return decrypted_data.decode('utf-8').strip() 
    except UnicodeDecodeError:
        return decrypted_data  

