# helper function for comparing a 'true' dict to a response dict
def compare_data(ground_truth_data: dict, response_data: dict):
    for key in ground_truth_data:
        if ground_truth_data[key] != response_data.get(key):
            return False
    return True





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
