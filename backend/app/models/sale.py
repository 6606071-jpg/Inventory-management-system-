from app.utils.db import execute_query
from datetime import datetime

class Sale:
    """Sale model"""
    
    @staticmethod
    def create(product_id, quantity, total_price, customer_name, payment_method):
        """Record a sale"""
        query = """
        INSERT INTO sales (product_id, quantity, total_price, customer_name, payment_method, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        params = (product_id, quantity, total_price, customer_name, payment_method, datetime.now())
        return execute_query(query, params)
    
    @staticmethod
    def get_all():
        """Get all sales"""
        query = """
        SELECT s.*, p.name, p.sku FROM sales s
        JOIN products p ON s.product_id = p.id
        ORDER BY s.created_at DESC
        """
        return execute_query(query, fetch=True)
    
    @staticmethod
    def get_by_id(sale_id):
        """Get sale by ID"""
        query = """
        SELECT s.*, p.name, p.sku FROM sales s
        JOIN products p ON s.product_id = p.id
        WHERE s.id = ?
        """
        result = execute_query(query, (sale_id,), fetch=True)
        return result[0] if result else None
    
    @staticmethod
    def get_by_date_range(start_date, end_date):
        """Get sales within date range"""
        query = """
        SELECT s.*, p.name, p.sku FROM sales s
        JOIN products p ON s.product_id = p.id
        WHERE date(s.created_at) BETWEEN ? AND ?
        ORDER BY s.created_at DESC
        """
        return execute_query(query, (start_date, end_date), fetch=True)
    
    @staticmethod
    def get_total_sales(start_date=None, end_date=None):
        """Get total sales amount"""
        if start_date and end_date:
            query = """
            SELECT SUM(total_price) as total FROM sales
            WHERE date(created_at) BETWEEN ? AND ?
            """
            result = execute_query(query, (start_date, end_date), fetch=True)
        else:
            query = "SELECT SUM(total_price) as total FROM sales"
            result = execute_query(query, fetch=True)
        
        return result[0]['total'] if result else 0
