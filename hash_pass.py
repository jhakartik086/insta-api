import hashlib

# Hash password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()