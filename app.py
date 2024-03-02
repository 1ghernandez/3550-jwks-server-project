from flask import Flask, request, jsonify
from datetime import datetime, timedelta #for the date and time 
from keyManager import rsa_key, keysStorage  # Import the function and storage from keyManager script
import jwt
import base64
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend

# Creates an expired key from an existing one to see if it catches expired keys. 
#some_kid = list(keysStorage.keys())[0]  # Get the kid of the first key as an example
#keysStorage[some_kid]["Expiry"] = datetime.now() - timedelta(days=1)  # Set its expiry to one day in the past
# website for server: http://127.0.0.1:8080/.well-known/jwks.json

#initialize flask
app = Flask(__name__)
# for the server
@app.route("/.well-known/jwks.json", methods=["GET"])
#function for jwks server, returns non expired keys 
def jwks():
    non_expired_keys = []
    # Checks if keys are expired or not
    for kid, key_info in keysStorage.items():
        if key_info["Expiry"] > datetime.now():
            # Deserializes public key from PEM format
            public_key = serialization.load_pem_public_key(
                key_info["Public Key"],
                backend=default_backend()
            )
            # Ensures the public key is RSA type, then extracts modulus and exponent for JWK format
            if isinstance(public_key, rsa.RSAPublicKey):
                public_numbers = public_key.public_numbers()
                modulus = public_numbers.n
                exponent = public_numbers.e
                
                jwk = {
                    "kty": "RSA",
                    "use": "sig",
                    "kid": kid,
                    "alg": "RS256",
                    "n": base64.urlsafe_b64encode(modulus.to_bytes((modulus.bit_length() + 7) // 8, byteorder='big')).rstrip(b'=').decode('utf-8'),
                    "e": base64.urlsafe_b64encode(exponent.to_bytes((exponent.bit_length() + 7) // 8, byteorder='big')).rstrip(b'=').decode('utf-8'),
                }
                non_expired_keys.append(jwk)
    
    return jsonify({"keys": non_expired_keys})

@app.route("/auth", methods=["POST"])
def auth():
    use_expired = "expired" in request.args
    # Find a key to use - here we don't care if the key is expired, we only care about the token's 'exp'
    for kid, key_info in keysStorage.items():
        private_key = serialization.load_pem_private_key(
            key_info["Private Key"],
            password=None,
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
        token = jwt.encode(payload, private_key, algorithm="RS256", headers={"kid": kid})
        return jsonify({"token": token})

    return jsonify({"error": "No suitable key found"}), 400

@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify(error="Method Not Allowed"), 405

if __name__ == "__main__":
    app.run(port=8080)