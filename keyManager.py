from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import uuid
from datetime import datetime, timedelta


 # in-memory storage
keysStorage = {}

# Function to generate an RSA key pair
def rsa_key():
    # Generate private key
    privateKey = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()

    )

    # Expires after 1 year
    expires = datetime.now() + timedelta(days = 365)

    # Generates the public key
    publicKey = privateKey.public_key()

    # Generates a unique Key ID (kid)
    kID = str(uuid.uuid4())

    # Creates private key to PEM format
    pemPrivate = privateKey.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    # Creates public key to PEM format
    pemPublic = publicKey.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Stores the keys along with kid and expiry in the keys storage
    keysStorage[kID] = {
        "Private Key": pemPrivate,
        "Public Key": pemPublic,
        "Expiry": expires
    }
    
    return kID, pemPublic, expires

# Prints the keys
kID, publicKey, expiry = rsa_key()
print(f"Generated key with kid: {kID} \nand expiry: {expiry}\n")
print("Public Key:", publicKey.decode())
