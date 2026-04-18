from flask import Blueprint, request, jsonify
from app.models.purchase import Purchase
from app.models.product import Product

bp = Blueprint('purchases', __name__, url_prefix='/api/purchases')

@bp.route('', methods=['GET'])
def get_purchases():
    """Get all purchases"""
    try:
        purchases = Purchase.get_all()
        return jsonify(purchases), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:purchase_id>', methods=['GET'])
def get_purchase(purchase_id):
    """Get purchase by ID"""
    try:
        purchase = Purchase.get_by_id(purchase_id)
        if not purchase:
            return jsonify({'error': 'Purchase not found'}), 404
        return jsonify(purchase), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('', methods=['POST'])
def create_purchase():
    """Create new purchase"""
    try:
        data = request.get_json()
        
        required_fields = ['product_id', 'quantity', 'purchase_price', 'supplier_name']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Get product details
        product = Product.get_by_id(data['product_id'])
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        quantity = int(data['quantity'])
        
        # Create purchase record
        Purchase.create(
            product_id=data['product_id'],
            quantity=quantity,
            purchase_price=float(data['purchase_price']),
            supplier_name=data['supplier_name'],
            notes=data.get('notes', '')
        )
        
        # Update product stock
        new_quantity = product['quantity'] + quantity
        Product.update(data['product_id'], quantity=new_quantity)
        
        return jsonify({'message': 'Purchase recorded successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/date-range', methods=['GET'])
def get_purchases_by_date():
    """Get purchases by date range"""
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        if not start_date or not end_date:
            return jsonify({'error': 'Missing date parameters'}), 400
        
        purchases = Purchase.get_by_date_range(start_date, end_date)
        return jsonify(purchases), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/total', methods=['GET'])
def get_total_purchases():
    """Get total purchases"""
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        total = Purchase.get_total_purchases(start_date, end_date)
        return jsonify({'total': total}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
