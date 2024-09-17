import pytest
import json
from datetime import datetime
from run import app  # Import the app from run.py
from src.models import Blog  # Import the Blog model from src/models.py
from src import db  # Import the db object from src/__init__.py

test_blog_data_1 = {
    "title": "Discussing the book Emma by Jane Austen",
    "author": "Daniel Drew",
    "date": datetime.today().strftime("%y-%m-%d"),
    "content": """Emma is a novel written by English author Jane Austen. It is set in the fictional country village of Highbury and 
                        the surrounding estates of Hartfield, Randalls and Donwell Abbey, 
                        and involves the relationships among people from a small number of families.""",
}

test_blog_data_2 = {
    "title": "Discussing the book Pride and Prejudice by Jane Austen",
    "author": "Daniel Drew",
    "date": datetime.today().strftime("%y-%m-%d"),
    "content": """Pride and Prejudice is an 1813 romantic novel of manners written by Jane Austen. 
                        The novel follows the character development of Elizabeth Bennet, the dynamic protagonist of the book who learns 
                        about the repercussions of hasty judgments and comes to appreciate the difference between superficial goodness 
                        and actual goodness.""",
}


@pytest.fixture
def client():
    # Pre-test setup
    print("Setting up app for testing")

    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"  # Use an in-memory SQLite database for testing
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Create the test client and test database
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Create the database schema

        yield client  # Run the tests

        # Post-test cleanup
        with app.app_context():
            db.session.remove()
            db.drop_all()  # Drop all tables after the test

    print("Tearing app down after testing")


def test_get_empty_blogs_list(client):
    """Test for getting an empty list of blogs

    Args:
        client (FlaskClient): a flask test client
    """
    response = client.get("/blogs")
    assert response.status_code == 200
    assert response.json == []


def test_post_valid_blog(client):
    """Test for posting a blog and retrieving it

    Args:
        client (FlaskClient): a flask test client
    """

    # Post a new blog
    post_response = client.post("/blogs", json=test_blog_data_1)
    # Check the immediate response
    assert post_response.status_code == 201
    assert post_response.json["title"] == test_blog_data_1["title"]

    # Retrieve the posted blog using GET method
    get_response = client.get("/blogs")
    assert get_response.status_code == 200
    assert any(blog['title'] == test_blog_data_1["title"] for blog in get_response.json)


def test_post_and_retrieve_multiple_blogs(client):
    """Test for posting multiple blogs and retrieving them

    Args:
        client (FlaskClient): a flask test client
    """

    # Post the first blog
    post_response = client.post("/blogs", json=test_blog_data_1)
    assert post_response.status_code == 201
    assert post_response.json["title"] == test_blog_data_1["title"]

    # Post the second blog
    post_response = client.post("/blogs", json=test_blog_data_2)
    assert post_response.status_code == 201
    assert post_response.json["title"] == test_blog_data_2["title"]

    # Retrieve the posted blogs using GET method
    get_response = client.get("/blogs")
    assert get_response.status_code == 200
    assert any(blog['title'] == test_blog_data_1["title"] for blog in get_response.json)
    assert any(blog['title'] == test_blog_data_2["title"] for blog in get_response.json)
