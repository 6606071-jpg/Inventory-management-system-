from flask import Blueprint, request, jsonify
from app.models.product import Product
from app.utils.auth import hash_password, verify_password
import jwt
from datetime import datetime, timedelta
import os

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@bp.route('/login', methods=['POST'])
def login():
    """User login"""
    data = request.get_json()
    
    # Simple auth - in production use proper user model
    username = data.get('username')
    password = data.get('password')
    
    # Mock authentication
    if username == 'admin' and password == 'password':
        token = jwt.encode(
            {'user': username, 'exp': datetime.utcnow() + timedelta(hours=24)},
            os.getenv('SECRET_KEY', 'your-secret-key'),
            algorithm='HS256'
        )
        return jsonify({'token': token, 'message': 'Login successful'}), 200
    
    return jsonify({'message': 'Invalid credentials'}), 401

@bp.route('/logout', methods=['POST'])
def logout():
    """User logout"""
    return jsonify({'message': 'Logout successful'}), 200

@bp.route('/verify-token', methods=['GET'])
def verify_token():
    """Verify JWT token"""
    token = request.headers.get('Authorization')
    
    if not token:
        return jsonify({'message': 'No token provided'}), 401
    
    try:
        token = token.split(' ')[1]
        jwt.decode(token, os.getenv('SECRET_KEY', 'your-secret-key'), algorithms=['HS256'])
        return jsonify({'valid': True}), 200
    except:
        return jsonify({'valid': False, 'message': 'Invalid token'}), 401
