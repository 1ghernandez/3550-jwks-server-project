from flask import Flask, request, jsonify
from datetime import datetime, timedelta #for the date and time 
from keyManager import initialize_database, rsa_key, storeInDB
import jwt
import base64
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
import sqlite3
import logging

# website for server: http://127.0.0.1:8080/.well-known/jwks.json

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s') # for debugging

#initialize flask
app = Flask(__name__)

# initialize the database
initialize_database()

# create a pair of keys 
privateKey, pemPublic, expires = rsa_key()
# stores the keys private key in the database
kID = storeInDB(privateKey, expires)

# retrives teh public key from the private key
def getPublicKeyJWKS(private_key_pem):
    # Load the private key from PEM format
    private_key = serialization.load_pem_private_key(
        private_key_pem,
        password=None, 
        backend=default_backend()
    )

    # Get the public key
    public_key = private_key.public_key()

    # Serialize the public key to PEM format
    pem_public_key = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    return pem_public_key # returns the public key

# for the server
@app.route('/.well-known/jwks.json', methods=['GET'])
def jwks():
    try:
        # creates a connection to the database
        database_connection = sqlite3.connect('totally_not_my_privateKeys.db')
        cursor = database_connection.cursor() # creates a cursor to read and write 
        
        cursor.execute("SELECT kid, key FROM keys LIMIT 1") # sends a SQL query to the database and ensures only one row is retrieved
        row = cursor.fetchone() # retrieves the next row of a query result set
        database_connection.close() # close database connection

        if row:
            kid, pem_private_key = row

            # private key goes for PEM format to object 
            private_key = serialization.load_pem_private_key(
                pem_private_key,
                password=None,
                backend=default_backend()
            )
            public_key = private_key.public_key()
            public_numbers = public_key.public_numbers()

            # extracts modulus and exponent for JWK format
            jwks = {
                "keys": [
                    {
                        "kty": "RSA",
                        "use": "sig",
                        "kid": str(kid),
                        "n": base64.urlsafe_b64encode(public_numbers.n.to_bytes((public_numbers.n.bit_length() + 7) // 8, byteorder='big')).decode('utf-8').rstrip("="),
                        "e": base64.urlsafe_b64encode(public_numbers.e.to_bytes((public_numbers.e.bit_length() + 7) // 8, byteorder='big')).decode('utf-8').rstrip("="),
                    }
                ]
            }
            
            return jsonify(jwks)
        else:
            return jsonify({"error": "Key not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/auth", methods=["POST"])
def auth():
    use_expired = "expired" in request.args

    # first gets the key from the database
    database_connection = sqlite3.connect('totally_not_my_privateKeys.db')
    cursor = database_connection.cursor()

    if use_expired:
         # Set token to expire in the past
        cursor.execute("SELECT kid, key FROM keys WHERE exp < ?", (datetime.now().timestamp(),))
    else:
        # Set token to expire in the future
        cursor.execute("SELECT kid, key FROM keys WHERE exp > ?", (datetime.now().timestamp(),))

    print("Fetching a key from the database...") # for debugging
    key_record = cursor.fetchone() # saves the key in key_record

    database_connection.close()

    # if key_record exists
    if key_record: 
        # put in PEM format
        kid, pem_private_key = key_record
        private_key = serialization.load_pem_private_key(
            pem_private_key,
            password=None,
            backend=default_backend()
        )

        if use_expired:
            # Set token to expire in the past
            payload = {
                "iss": "YourIssuer",
                "exp": datetime.utcnow() - timedelta(minutes=5),
            }
        else:
            # Set token to expire in the future
            payload = {
                "iss": "YourIssuer",
                "exp": datetime.utcnow() + timedelta(minutes=5),
            }

        token = jwt.encode(payload, private_key, algorithm="RS256", headers={"kid": str(kid)})
        #print(f"Generated JWT: {token}") # for debugging 
        return jsonify({"token": token})

    return jsonify({"error": "No suitable key found"}), 400

# for errors 
@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify(error="Method Not Allowed"), 405

#runs flask on port 8080
if __name__ == "__main__":
    app.run(debug=True, port=8080)