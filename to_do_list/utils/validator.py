import re

"""_summary_
validateUserName is a function that validates a username
:param username: the username to validate
:return: a string with the error message if the username is invalid, an empty string otherwise
example:
validateUserName("user") -> "Username must have at least 6 characters"
validateUserName("username") -> ""
validateUserName("usernameusernameusernameusername") -> "Username must have at most 20 characters"
"""
def validateUserName(username:str) -> str:
    if len(username) < 6:
        return "Username must have at least 6 characters"
    if len(username) > 20:
        return "Username must have at most 20 characters"
    return ""

"""_summary_
validateEmail is a function that validates an email
:param email: the email to validate
:return: True if the email is valid, False otherwise
example:
validateEmail("email") -> False
validateEmail("") -> False
validateEmail("example@example.com") -> True
"""
def validateEmail(email:str)->bool:
    expresion_regular = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
    return re.match(expresion_regular, email) is not None

"""_summary_
validatePassword is a function that validates a password
:param password: the password to validate
:return: a string with the error message if the password is invalid, an empty string otherwise
example:
validatePassword("password") -> "Password must have at least 8 characters"
validatePassword("password1") -> "Password must have at least one uppercase letter"
validatePassword("Password1") -> ""
"""
def validatePassword(password:str)->str:
    if len(password) < 8:
        return "Password must have at least 8 characters"
    if not any(char.isdigit() for char in password):
        return "Password must have at least one number"
    if not any(char.isupper() for char in password):
        return "Password must have at least one uppercase letter"
    return ""