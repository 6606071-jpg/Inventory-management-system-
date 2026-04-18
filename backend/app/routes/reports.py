from flask import Blueprint, request, jsonify
from app.models.sale import Sale
from app.models.purchase import Purchase
from app.models.product import Product

bp = Blueprint('reports', __name__, url_prefix='/api/reports')

@bp.route('/sales-report', methods=['GET'])
def sales_report():
    """Generate sales report"""
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        if not start_date or not end_date:
            return jsonify({'error': 'Missing date parameters'}), 400
        
        sales = Sale.get_by_date_range(start_date, end_date)
        total = Sale.get_total_sales(start_date, end_date)
        
        return jsonify({
            'total_sales': total,
            'transaction_count': len(sales) if sales else 0,
            'sales': sales
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/purchase-report', methods=['GET'])
def purchase_report():
    """Generate purchase report"""
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        if not start_date or not end_date:
            return jsonify({'error': 'Missing date parameters'}), 400
        
        purchases = Purchase.get_by_date_range(start_date, end_date)
        total = Purchase.get_total_purchases(start_date, end_date)
        
        return jsonify({
            'total_purchases': total,
            'transaction_count': len(purchases) if purchases else 0,
            'purchases': purchases
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/profit-analysis', methods=['GET'])
def profit_analysis():
    """Generate profit analysis report"""
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        if not start_date or not end_date:
            return jsonify({'error': 'Missing date parameters'}), 400
        
        total_sales = Sale.get_total_sales(start_date, end_date)
        total_purchases = Purchase.get_total_purchases(start_date, end_date)
        profit = (total_sales or 0) - (total_purchases or 0)
        margin = ((profit / total_sales) * 100) if total_sales else 0
        
        return jsonify({
            'total_sales': total_sales,
            'total_purchases': total_purchases,
            'profit': profit,
            'profit_margin': f"{margin:.2f}%"
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/stock-report', methods=['GET'])
def stock_report():
    """Generate stock report"""
    try:
        products = Product.get_all()
        total_value = sum((p.get('price', 0) or 0) * (p.get('quantity', 0) or 0) for p in products) if products else 0
        
        return jsonify({
            'total_products': len(products) if products else 0,
            'total_stock_value': total_value,
            'products': products
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/dashboard', methods=['GET'])
def dashboard():
    """Get dashboard metrics"""
    try:
        products = Product.get_all()
        low_stock_products = Product.get_low_stock(10)
        total_sales = Sale.get_total_sales()
        
        return jsonify({
            'total_products': len(products) if products else 0,
            'low_stock_alerts': len(low_stock_products) if low_stock_products else 0,
            'total_sales': total_sales,
            'low_stock_items': low_stock_products
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
