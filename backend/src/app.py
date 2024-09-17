from flask import Flask
from src.db import db

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blogs.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    # Create the database tables (if they don't exist)
    with app.app_context():
        db.create_all()

    from src.routes import blog_routes
    app.register_blueprint(blog_routes)

    return app