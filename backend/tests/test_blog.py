import pytest
import json
from flask import Flask
from src.db import Blog, User, db
from src.app import create_test_db, add_routes
from tests.utils import *
from tests.data import *



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


# TESTS:

# check we can add users and then retrieve them with get '/users'
def test_get_users(client):
    user_1 = create_user(client, test_user_data_1)
    user_2 = create_user(client, test_user_data_2)

    check_user_exists_in_get_users(client, user_1)
    check_user_exists_in_get_users(client, user_2)



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



