import sqlite3
import os
from flask import current_app
from contextlib import contextmanager

def get_db_connection():
    """Get SQLite database connection"""
    try:
        db_path = current_app.config['DATABASE_PATH']
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        print(f"Error connecting to SQLite: {e}")
        return None

def init_db(app):
    """Initialize database with schema"""
    with app.app_context():
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
                # Get the project root directory (go up 4 levels from this file)
                current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
                schema_path = os.path.join(current_dir, 'database', 'schema.sql')
                seed_path = os.path.join(current_dir, 'database', 'seed_data.sql')
                
                with open(schema_path, 'r') as schema_file:
                    schema = schema_file.read()
                    # SQLite doesn't support multiple statements, so split and execute
                    for statement in schema.split(';'):
                        if statement.strip():
                            cursor.execute(statement)
                conn.commit()
                print("✓ Database initialized successfully")
                
                # Insert seed data
                with open(seed_path, 'r') as seed_file:
                    seed = seed_file.read()
                    for statement in seed.split(';'):
                        if statement.strip():
                            cursor.execute(statement)
                conn.commit()
                print("✓ Sample data loaded")
            except Exception as e:
                print(f"Error initializing database: {e}")
            finally:
                cursor.close()
                conn.close()

def execute_query(query, params=None, fetch=False):
    """Execute database query"""
    conn = get_db_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        if fetch:
            result = [dict(row) for row in cursor.fetchall()]
        else:
            conn.commit()
            result = cursor.rowcount
        
        cursor.close()
        conn.close()
        return result
    except Exception as e:
        print(f"Database error: {e}")
        return None
