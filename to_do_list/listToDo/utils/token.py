import jwt
from datetime import datetime, timedelta

from dotenv import dotenv_values

"""_summary_
generateJWT is a function that generates a JWT token
:param username: the username to include in the token
:param email: the email to include in the token
:param hashPassword: the hash password to include in the token
:return: a JWT token
example:
generateJWT("user", "email","hashPassword") -> "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InVzZXIiLCJlbWFpbCI6ImVtYWlsIiwiaGFzaFBhc3N3b3JkIjoiaGFzaFBhc3N3b3JkIiwiZXhwIjoxNjI5MjIwNzIyfQ.
"""
def generateJWT(username:str, email:str, hashPassword)->str:
    payload = {
        'username': username,
        'email': email,
        'hashPassword': hashPassword,
        'exp': datetime.now() + timedelta(weeks=4)
    }
    return jwt.encode(payload, str(dotenv_values(".env.SECRET")), algorithm='HS256')