from flask import Blueprint, request, jsonify
from app.models.product import Product
from flask import current_app

bp = Blueprint('products', __name__, url_prefix='/api/products')

@bp.route('', methods=['GET'])
def get_products():
    """Get all products"""
    try:
        products = Product.get_all()
        return jsonify(products), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get product by ID"""
    try:
        product = Product.get_by_id(product_id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        return jsonify(product), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('', methods=['POST'])
def create_product():
    """Create new product"""
    try:
        data = request.get_json()
        
        required_fields = ['name', 'price', 'sku', 'quantity']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        result = Product.create(
            name=data['name'],
            description=data.get('description', ''),
            price=float(data['price']),
            sku=data['sku'],
            quantity=int(data['quantity']),
            category=data.get('category', '')
        )
        
        return jsonify({'message': 'Product created successfully', 'id': result}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """Update product"""
    try:
        data = request.get_json()
        
        # Convert price and quantity to correct types if present
        if 'price' in data:
            data['price'] = float(data['price'])
        if 'quantity' in data:
            data['quantity'] = int(data['quantity'])
        
        result = Product.update(product_id, **data)
        
        if result == 0:
            return jsonify({'error': 'Product not found'}), 404
        
        return jsonify({'message': 'Product updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Delete product"""
    try:
        result = Product.delete(product_id)
        
        if result == 0:
            return jsonify({'error': 'Product not found'}), 404
        
        return jsonify({'message': 'Product deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/low-stock', methods=['GET'])
def get_low_stock():
    """Get products with low stock"""
    try:
        threshold = request.args.get('threshold', default=current_app.config['STOCK_ALERT_THRESHOLD'], type=int)
        products = Product.get_low_stock(threshold)
        return jsonify(products), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
