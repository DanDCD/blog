from flask import Flask
from sqlalchemy import create_engine, text
from src.db import db
from dotenv import load_dotenv
import os

# get the environment variables
load_dotenv()
local_db_host = os.getenv("LOCAL_DB_HOST")
local_db_port = os.getenv("LOCAL_DB_PORT")
local_db_username = os.getenv("LOCAL_DB_USERNAME")
local_db_password = os.getenv("LOCAL_DB_PASSWORD")
local_db_name = os.getenv("LOCAL_DB_NAME")
local_test_db_name = os.getenv("LOCAL_TEST_DB_NAME")

# create the Flask app
app = Flask(__name__)


def create_local_db(app):
    # we need to create the database locally if it doesn't exist yet
    engine = create_engine(
        f"mysql://{local_db_username}:{local_db_password}@{local_db_host}"
    )
    with engine.connect() as connection:
        connection.execute(text(f"CREATE DATABASE IF NOT EXISTS {local_db_name}"))
    engine.dispose()
    # now we can connect sql_alchemy to the database
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"mysql://{local_db_username}:{local_db_password}@{local_db_host}:{local_db_port}/{local_db_name}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    # if the tables don't exist, create them
    with app.app_context():
        db.create_all()


def create_test_db(app):
    # we need to create the test database locally if it doesn't exist yet
    engine = create_engine(f"mysql://{local_db_username}:{local_db_password}@{local_db_host}")
    with engine.connect() as connection:
        connection.execute(text(f"CREATE DATABASE IF NOT EXISTS {local_test_db_name}"))
    engine.dispose()
    # now we can connect sql_alchemy to the test database
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"mysql://{local_db_username}:{local_db_password}@{local_db_host}:{local_db_port}/{local_test_db_name}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    # if the tables don't exist, create them
    with app.app_context():
        db.drop_all()  # when testing, we want to start with a fresh database each test, so we drop all tables
        db.create_all()  # then we create the tables again


def add_routes(app):
    from src.routes import blog_routes
    from src.routes import user_routes

    app.register_blueprint(blog_routes)
    app.register_blueprint(user_routes)
