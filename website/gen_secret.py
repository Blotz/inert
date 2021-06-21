import os
import binascii
# Generates a random 24 bit string 
secret_key_value = os.urandom(24)
# Create the hex-encoded string value.
secret_key_value_hex_encoded = binascii.hexlify(secret_key_value)
# Set the SECRET_KEY value in Flask application configuration settings.
print(secret_key_value_hex_encoded)