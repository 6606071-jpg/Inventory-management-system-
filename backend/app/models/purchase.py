from app.utils.db import execute_query
from datetime import datetime

class Purchase:
    """Purchase model"""
    
    @staticmethod
    def create(product_id, quantity, purchase_price, supplier_name, notes):
        """Record a purchase"""
        query = """
        INSERT INTO purchases (product_id, quantity, purchase_price, supplier_name, notes, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        params = (product_id, quantity, purchase_price, supplier_name, notes, datetime.now())
        return execute_query(query, params)
    
    @staticmethod
    def get_all():
        """Get all purchases"""
        query = """
        SELECT p.*, pr.name, pr.sku FROM purchases p
        JOIN products pr ON p.product_id = pr.id
        ORDER BY p.created_at DESC
        """
        return execute_query(query, fetch=True)
    
    @staticmethod
    def get_by_id(purchase_id):
        """Get purchase by ID"""
        query = """
        SELECT p.*, pr.name, pr.sku FROM purchases p
        JOIN products pr ON p.product_id = pr.id
        WHERE p.id = ?
        """
        result = execute_query(query, (purchase_id,), fetch=True)
        return result[0] if result else None
    
    @staticmethod
    def get_by_date_range(start_date, end_date):
        """Get purchases within date range"""
        query = """
        SELECT p.*, pr.name, pr.sku FROM purchases p
        JOIN products pr ON p.product_id = pr.id
        WHERE date(p.created_at) BETWEEN ? AND ?
        ORDER BY p.created_at DESC
        """
        return execute_query(query, (start_date, end_date), fetch=True)
    
    @staticmethod
    def get_total_purchases(start_date=None, end_date=None):
        """Get total purchase amount"""
        if start_date and end_date:
            query = """
            SELECT SUM(purchase_price * quantity) as total FROM purchases
            WHERE date(created_at) BETWEEN ? AND ?
            """
            result = execute_query(query, (start_date, end_date), fetch=True)
        else:
            query = "SELECT SUM(purchase_price * quantity) as total FROM purchases"
            result = execute_query(query, fetch=True)
        
        return result[0]['total'] if result else 0
