import pytest
import json
from flask import Flask
from src.db import Blog, User, db
from src.app import create_test_db, add_routes

# Test data for blogs and users
test_blog_data_1 = {
    "title": "Discussing the book Emma by Jane Austen",
    "author_id": None,
    "content": """Emma is a novel written by English author Jane Austen. It is set in the fictional country village of Highbury and 
                  the surrounding estates of Hartfield, Randalls, and Donwell Abbey.""",
}

test_blog_data_2 = {
    "title": "Discussing the book Pride and Prejudice by Jane Austen",
    "author_id": None,
    "content": """Pride and Prejudice is an 1813 romantic novel of manners written by Jane Austen. 
                  The novel follows Elizabeth Bennet and the repercussions of hasty judgments.""",
}

test_user_data_1 = {"username": "Gru", "password": "iloveminions"}
test_user_data_2 = {"username": "Vector", "password": "dir+mag"}


# helper function for comparing a 'true' dict to a response dict
def compare_data(ground_truth_data: dict, response_data: dict):
    for key in ground_truth_data:
        if ground_truth_data[key] != response_data.get(key):
            return False
    return True


# fixtures set up and tear down each test
@pytest.fixture
def client():
    app = Flask(__name__)
    create_test_db(app)
    add_routes(app)

    with app.test_client() as client:
        with app.app_context():
            yield client  # this is where the test will run
            db.session.remove()
            db.drop_all()


# helper function to create user
def create_user(client, user_data):
    response = client.post("/users", json=user_data)
    assert response.status_code == 201
    return response.json


# helper function to create blog
def post_blog(client, blog_data):
    response = client.post("/blogs", json=blog_data)
    assert response.status_code == 201
    return response.json


# helper function to check that a blog exists using get /blogs
def check_blog_exists_in_get_blogs(client, blog_data):
    response = client.get("/blogs")
    assert response.status_code == 200

    blogs_with_title = [
        blog for blog in response.json if blog["title"] == blog_data["title"]
    ]
    assert len(blogs_with_title) == 1 and compare_data(blog_data, blogs_with_title[0])


def check_user_exists_in_get_users(client, user_data):
    response = client.get("/users")
    assert response.status_code == 200

    users_with_name = [
        user for user in response.json if user["username"] == user_data["username"]
    ]
    assert len(users_with_name) == 1 and compare_data(user_data, users_with_name[0])


# test for retrieving blogs when none exist
def test_get_empty_blogs_list(client):
    response = client.get("/blogs")
    assert response.status_code == 200
    assert response.json == []


# test for posting and retrieving a single blog
def test_post_valid_blog(client):
    user_id = create_user(client, test_user_data_1)["id"]

    blog_data = test_blog_data_1.copy()
    blog_data["author_id"] = user_id
    assert compare_data(blog_data, post_blog(client, blog_data))

    # check the blog can be retrieved from get /blogs
    check_blog_exists_in_get_blogs(client, blog_data)


# test for posting and retrieving multiple blogs
def test_post_and_retrieve_multiple_blogs(client):
    user_id = create_user(client, test_user_data_1)["id"]

    blog_data_1 = test_blog_data_1.copy()
    blog_data_1["author_id"] = user_id
    assert compare_data(blog_data_1, post_blog(client, blog_data_1))

    blog_data_2 = test_blog_data_2.copy()
    blog_data_2["author_id"] = user_id
    assert compare_data(blog_data_2, post_blog(client, blog_data_2))

    check_blog_exists_in_get_blogs(client, blog_data_1)
    check_blog_exists_in_get_blogs(client, blog_data_2)


def test_get_user_by_username(client):
    user_1 = create_user(client, test_user_data_1)
    user_2 = create_user(client, test_user_data_2)

    check_user_exists_in_get_users(client, user_1)
    check_user_exists_in_get_users(client, user_2)