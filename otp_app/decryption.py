from Crypto.Cipher import AES
from base64 import b64decode

def decrypt_data(encrypted_data, secret_key):
    key = secret_key[:16]
    decoded_encrypted_data = b64decode(encrypted_data)
    cipher = AES.new(key, AES.MODE_ECB) 
    decrypted_data = cipher.decrypt(decoded_encrypted_data)
    return decrypted_data.strip()
