# 3550-jwks-server-project
Implementing a basic JWKS Server

### Name: Gloria Hernández
### EUID: gih0006
### Class: CSCE 3550.002

## Before Beginning 
- Install Python 3.11.4 or newer
- Install Flask
- Install pyJWT
- Install cryptography library for python

## How to Run
1. Clone the Repository
    git clone https://github.com/1ghernandez/3550-jwks-server-project.git
2. Install the required programs
3. From your terminal/console start the server by using
    "python3 app.py" or "python app.py"
    NOTE: The python you use depends on if you have various versions of python downloaded. 
    For example, if you have python 2 and 3 downloaded then use "python3 app.py" otherwise just use "python app.py".
4.  Once server is running you may go to this link: 
    http://127.0.0.1:8080/.well-known/jwks.json in your web browser to view the JSON Web Key.

## Testing
To test I used pytest. 
In your terminal/console use the command "pytest" to test the test suite. 
NOTE: Ensure when you use pytest, you are in the directory in which the repository exists.
