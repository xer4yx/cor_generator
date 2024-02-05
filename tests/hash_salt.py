import bcrypt as bc
import os

salt = bc.gensalt()

input_password = "nugga"
password = "mypassword"

hashed_password = bc.hashpw(password.encode('utf-8'), salt)

salt_storage = salt.decode('utf-8')
hashed_password_storage = hashed_password.decode('utf-8')

if bc.checkpw(input_password.encode('utf-8'), hashed_password):
    print("Password is correct")
else:
    print("Password is incorrect")
    print(salt)