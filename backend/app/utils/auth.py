import hashlib
import secrets

def hash_password(password):
    """Hash password with salt"""
    salt = secrets.token_hex(16)
    hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
    return f"{salt}${hashed.hex()}"

def verify_password(password, hashed):
    """Verify password against hash"""
    try:
        salt, hash_val = hashed.split('$')
        hashed_check = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        return hash_val == hashed_check.hex()
    except:
        return False

def generate_token():
    """Generate secure token"""
    return secrets.token_urlsafe(32)
