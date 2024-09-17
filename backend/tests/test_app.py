import pytest
import json
from datetime import datetime
from src.app import app


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

    # attempt to post a new blog
    post_response = client.post("/blogs", json=test_blog_data_1)
    # check the immediate response
    assert post_response.status_code == 201
    assert post_response.json == test_blog_data_1

    # attempt to retrieve the posted blog using GET method
    get_response = client.get("/blogs")
    assert get_response.status_code == 200
    assert test_blog_data_1 in get_response.json


def test_post_and_retrieve_multiple_blogs(client):
    """Test for posting multiple blogs and retrieving them

    Args:
        client (FlaskClient): a flask test client
    """
    
    # attempt to post a new blog
    post_response = client.post("/blogs", json=test_blog_data_1)
    # check the immediate response
    assert post_response.status_code == 201
    assert post_response.json == test_blog_data_1
    
    # attempt to post another blog
    post_response = client.post("/blogs", json=test_blog_data_2)
    # check the immediate response
    assert post_response.status_code == 201
    assert post_response.json == test_blog_data_2
    
    # attempt to retrieve the posted blogs using GET method
    get_response = client.get("/blogs")
    assert get_response.status_code == 200
    assert test_blog_data_1 in get_response.json
    assert test_blog_data_2 in get_response.json
