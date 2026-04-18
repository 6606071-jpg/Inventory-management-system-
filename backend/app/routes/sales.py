from flask import Blueprint, request, jsonify
from app.models.sale import Sale
from app.models.product import Product

bp = Blueprint('sales', __name__, url_prefix='/api/sales')

@bp.route('', methods=['GET'])
def get_sales():
    """Get all sales"""
    try:
        sales = Sale.get_all()
        return jsonify(sales), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:sale_id>', methods=['GET'])
def get_sale(sale_id):
    """Get sale by ID"""
    try:
        sale = Sale.get_by_id(sale_id)
        if not sale:
            return jsonify({'error': 'Sale not found'}), 404
        return jsonify(sale), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('', methods=['POST'])
def create_sale():
    """Create new sale"""
    try:
        data = request.get_json()
        
        required_fields = ['product_id', 'quantity', 'customer_name']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Get product details
        product = Product.get_by_id(data['product_id'])
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        # Check stock
        quantity = int(data['quantity'])
        if product['quantity'] < quantity:
            return jsonify({'error': 'Insufficient stock'}), 400
        
        # Calculate total price
        total_price = product['price'] * quantity
        
        # Create sale record
        Sale.create(
            product_id=data['product_id'],
            quantity=quantity,
            total_price=total_price,
            customer_name=data['customer_name'],
            payment_method=data.get('payment_method', 'cash')
        )
        
        # Update product stock
        new_quantity = product['quantity'] - quantity
        Product.update(data['product_id'], quantity=new_quantity)
        
        return jsonify({'message': 'Sale recorded successfully', 'total_price': total_price}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/date-range', methods=['GET'])
def get_sales_by_date():
    """Get sales by date range"""
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        if not start_date or not end_date:
            return jsonify({'error': 'Missing date parameters'}), 400
        
        sales = Sale.get_by_date_range(start_date, end_date)
        return jsonify(sales), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/total', methods=['GET'])
def get_total_sales():
    """Get total sales"""
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        total = Sale.get_total_sales(start_date, end_date)
        return jsonify({'total': total}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
