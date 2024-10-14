from Crypto.Cipher import AES
from base64 import b64decode

def decrypt_data(encrypted_data, secret_key):
    # Convert the secret key to 16 bytes (AES block size)
    key = secret_key[:16]
    
    # Decode the base64-encoded string
    decoded_encrypted_data = b64decode(encrypted_data)
    
    # Initialize the AES cipher
    cipher = AES.new(key, AES.MODE_ECB)  # or you can use other AES modes like CBC, CTR, etc.

    # Decrypt the data
    decrypted_data = cipher.decrypt(decoded_encrypted_data)

    # Return the decrypted string (might need to decode or strip padding)
    return decrypted_data.strip()
