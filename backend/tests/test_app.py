import pytest
import json
from datetime import datetime
from src.app import app


@pytest.fixture
def client():
    # pre-test
    print("Setting up app for testing")

    with app.test_client() as client:

        app.config["TESTING"] = True

        yield client  # run test now

    # post-test
    print("tearing app down after testing")


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
    blog_data = {
        "title": "Discussing the book Emma by Jane Austen",
        "author": "Daniel Drew",
        "date": datetime.today().strftime("%y-%m-%d"),
        "content": """Emma is a novel written by English author Jane Austen. It is set in the fictional country village of Highbury and 
                        the surrounding estates of Hartfield, Randalls and Donwell Abbey, 
                        and involves the relationships among people from a small number of families.""",
    }

    # attempt to post a new blog
    post_response = client.post("/blogs", json=blog_data)
    # check the immediate response
    assert post_response.status_code == 201
    assert post_response.json == blog_data

    # attempt to retrieve the posted blog using GET method
    get_response = client.get("/blogs")
    assert get_response.status_code == 200
    assert blog_data in get_response.json
