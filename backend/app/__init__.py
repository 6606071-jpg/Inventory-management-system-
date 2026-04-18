from flask import Flask
from flask_cors import CORS
from app.utils.db import init_db

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    
    # Enable CORS
    CORS(app)
    
    # Initialize database
    init_db(app)
    
    # Register blueprints
    from app.routes import products, sales, purchases, reports, auth
    app.register_blueprint(products.bp)
    app.register_blueprint(sales.bp)
    app.register_blueprint(purchases.bp)
    app.register_blueprint(reports.bp)
    app.register_blueprint(auth.bp)
    
    return app
