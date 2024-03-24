from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import uuid
from datetime import datetime, timedelta
import sqlite3
import os

# Function to generate an RSA key pair
def rsa_key():
    privateKey = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    expires = datetime.now() + timedelta(days=365) # keys expire after a year
    publicKey = privateKey.public_key() # public key that unlocks private key

    # preforms the serializations to match PEM format
    pemPublic = publicKey.public_bytes( 
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    return privateKey, pemPublic, expires

# function to read a private key from the file
def load_private_key_from_pem(pem_file_path):

    # Loads a private key from a PEM file.

    with open(pem_file_path, 'rb') as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None, 
            backend=default_backend()
        )
    return private_key

# function to read a public key from the file
def load_public_key_from_pem(pem_file_path):

    # Loads a public key from a PEM file.

    with open(pem_file_path, 'rb') as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )
    return public_key

# function to initialize a database
def initialize_database():
    print("Initializing database...")
    # with ensures that the database gets closed 
    with sqlite3.connect('totally_not_my_privateKeys.db') as database_connection:
        #print(f"Initializing/Accessing Database at {os.path.abspath('totally_not_my_privateKeys.db')}") # for debugging

        cursor = database_connection.cursor() # creates a cursor to read and write to the database
        
         # creating a table schema
        cursor.execute('''CREATE TABLE IF NOT EXISTS keys 
                       (kid INTEGER PRIMARY KEY AUTOINCREMENT, 
                       key BLOB NOT NULL, 
                       exp INTEGER NOT NULL
                       )''')
        database_connection.commit() # saves the database
        pass

# function to store the private key to the database
def store_in_DB(private_key, expiry): 
    with sqlite3.connect('totally_not_my_privateKeys.db') as database_connection:
        cursor = database_connection.cursor() # creates a cursor to read and write to the database

        # preforms the serializations to match PEM format
        pem_private_key = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        # changes the expiry format to match the table schema
        expiry_int = int(expiry.timestamp())

        # Executes the SQL INSERT statement
        cursor.execute("INSERT INTO keys (key, exp) VALUES (?, ?)", (pem_private_key, expiry_int))
        database_connection.commit() # saves the database

        return cursor.lastrowid # store ID of the last row or kID