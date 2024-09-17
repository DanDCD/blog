from flask import Flask
from src.db import db

app = Flask(__name__)

def create_prod_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blogs.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    # Create the database tables (if they don't exist)
    with app.app_context():
        db.create_all()

def create_test_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    # Create the database tables (if they don't exist)
    with app.app_context():
        db.create_all()

def add_routes(app):
    from src.routes import blog_routes
    app.register_blueprint(blog_routes)