from app.utils.db import execute_query
from datetime import datetime

class Product:
    """Product model"""
    
    @staticmethod
    def create(name, description, price, sku, quantity, category):
        """Create a new product"""
        query = """
        INSERT INTO products (name, description, price, sku, quantity, category, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        params = (name, description, price, sku, quantity, category, datetime.now())
        return execute_query(query, params)
    
    @staticmethod
    def get_all():
        """Get all products"""
        query = "SELECT * FROM products WHERE is_active = 1"
        return execute_query(query, fetch=True)
    
    @staticmethod
    def get_by_id(product_id):
        """Get product by ID"""
        query = "SELECT * FROM products WHERE id = ? AND is_active = 1"
        result = execute_query(query, (product_id,), fetch=True)
        return result[0] if result else None
    
    @staticmethod
    def update(product_id, **kwargs):
        """Update product"""
        allowed_fields = ['name', 'description', 'price', 'sku', 'quantity', 'category']
        updates = []
        params = []
        
        for key, value in kwargs.items():
            if key in allowed_fields:
                updates.append(f"{key} = ?")
                params.append(value)
        
        if not updates:
            return 0
        
        params.append(product_id)
        query = f"UPDATE products SET {', '.join(updates)} WHERE id = ?"
        return execute_query(query, params)
    
    @staticmethod
    def delete(product_id):
        """Soft delete product"""
        query = "UPDATE products SET is_active = 0 WHERE id = ?"
        return execute_query(query, (product_id,))
    
    @staticmethod
    def get_low_stock(threshold):
        """Get products with low stock"""
        query = "SELECT * FROM products WHERE quantity <= ? AND is_active = 1"
        return execute_query(query, (threshold,), fetch=True)
