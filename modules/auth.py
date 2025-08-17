import hashlib
from . import db 

def hash_password(password):
    """Hashes the password for secure storage."""
    return hashlib.sha256(password.encode()).hexdigest()

def add_user(username, password):
    """Hashes password and adds a new user to the database."""
    if not username or not password:
        return False # Ensure username and password are not empty
        
    hashed_pass = hash_password(password)
    return db.add_user_to_db(username, hashed_pass)

def check_user(username, password):
    """Checks if a user exists and the password is correct."""
    user = db.get_user_from_db(username)
    if user:
        hashed_pass = hash_password(password)
        if user['hashed_password'] == hashed_pass:
            return user['id'] # Return user ID on successful login
    return None # Return None if login fails