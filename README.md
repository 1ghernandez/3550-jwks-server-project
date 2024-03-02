# 3550-jwks-server-project
Implementing a basic JWKS Server

#### Name: Gloria Hernández
#### EUID: gih0006
#### Class: CSCE 3550.002

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
- To test I used pytest. 
- In your terminal/console use the command "pytest" to test the test suite. 
    - NOTE: Ensure when you use pytest, you are in the directory in which the repository exists.
 
## Screenshot of Test Suite
<img width="709" alt="Screenshot 2024-03-02 at 2 35 57 PM" src="https://github.com/1ghernandez/3550-jwks-server-project/assets/106200515/e71d2e11-ff8e-4f4a-98b4-7f12c60b1c71">

## Screenshot of Test Client
<img width="1002" alt="Screenshot 2024-03-02 at 3 17 59 PM" src="https://github.com/1ghernandez/3550-jwks-server-project/assets/106200515/16b718d0-0c68-4b31-a487-3a6720115d4a">



