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

    assert check_user_exists_in_get_users(client, user_1)
    assert check_user_exists_in_get_users(client, user_2)


# check we can create users and then retrieve them with get '/users/username'
def test_get_user_by_name(client):
    create_user(client, test_user_data_1)
    create_user(client, test_user_data_2)

    response_1 = client.get("/users/" + test_user_data_1["username"])
    assert response_1.status_code == 200
    assert test_user_data_1["username"] == response_1.json["username"]

    response_2 = client.get("/users/" + test_user_data_2["username"])
    assert response_2.status_code == 200
    assert test_user_data_2["username"] == response_2.json["username"]


# test we can post a new user with post '/users/'
def test_post_user(client):
    assert (
        create_user(client, test_user_data_1)["username"]
        == test_user_data_1["username"]
    )

# test we can create new users and delete them
def test_delete_user(client):
    user_1 = create_user(client, test_user_data_1)
    user_2 = create_user(client, test_user_data_2)
    
    response_1 = client.delete("/users/"+user_1['username'])
    assert response_1.status_code == 204
    assert not check_user_exists_in_get_users(client, test_user_data_1)
    
    response_2 = client.delete("/users/"+user_2['username'])
    assert response_2.status_code == 204
    assert not check_user_exists_in_get_users(client, test_user_data_2)


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
    assert check_blog_exists_in_get_blogs(client, blog_data)


# test for posting and retrieving multiple blogs
def test_post_and_retrieve_multiple_blogs(client):
    user_id = create_user(client, test_user_data_1)["id"]

    blog_data_1 = test_blog_data_1.copy()
    blog_data_1["author_id"] = user_id
    assert compare_data(blog_data_1, post_blog(client, blog_data_1))

    blog_data_2 = test_blog_data_2.copy()
    blog_data_2["author_id"] = user_id
    assert compare_data(blog_data_2, post_blog(client, blog_data_2))

    assert check_blog_exists_in_get_blogs(client, blog_data_1)
    assert check_blog_exists_in_get_blogs(client, blog_data_2)

# test for updating a blog with put '/blogs/blog_id'
def test_update_blog(client):
    # create a user
    user_id = create_user(client, test_user_data_1)["id"]
    
    # create a blog
    blog_data = test_blog_data_1.copy()
    blog_data["author_id"] = user_id
    blog = post_blog(client, blog_data)
    
    # update the blog
    updated_blog_data = test_blog_data_2.copy()
    updated_blog_data["author_id"] = user_id
    response = client.put("/blogs/"+str(blog['id']), json=updated_blog_data)
    assert response.status_code == 200
    assert compare_data(updated_blog_data, response.json)
    

# test for deleting a blod with delete '/blogs/blog_id'
def test_delete_blog(client):
    # create a user
    user_id = create_user(client, test_user_data_1)["id"]
    
    # create a blog
    blog_data = test_blog_data_1.copy()
    blog_data["author_id"] = user_id
    blog = post_blog(client, blog_data)
    
    # delete the blog
    response = client.delete("/blogs/"+str(blog['id']))
    assert response.status_code == 204
    assert not check_blog_exists_in_get_blogs(client, blog_data)