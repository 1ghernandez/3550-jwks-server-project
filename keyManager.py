from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import uuid
from datetime import datetime, timedelta


 # in-memory storage
keysStorage = {}

# Function to generate an RSA key pair
def generate_rsa_key_pair():
    # Generate private key
    privateKey = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()

    )

    # Expires after 1 year
    expires = datetime.now() + timedelta(days = 365)

    # Generate the public key
    publicKey = privateKey.public_key()

    # Generate a unique Key ID (kid)
    kID = str(uuid.uuid4())

    # Create private key to PEM format
    pemPrivate = privateKey.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    # Create public key to PEM format
    pemPublic = publicKey.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Store the keys along with kid and expiry in the keys storage
    keysStorage[kID] = {
        "Private Key": pemPrivate,
        "Public Key": pemPublic,
        "Expiry": expires
    }
    
    return kID, pemPublic, expires

# Print the keys to see them
kID, publicKey, expiry = generate_rsa_key_pair()
print(f"Generated key with kid: {kID} and expiry: {expiry}")
print("Public Key:", publicKey.decode())
