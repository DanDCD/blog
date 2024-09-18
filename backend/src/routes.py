from flask import request, jsonify, Blueprint
from src.db import Blog
from src.db import User
from src.db import db

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/users', methods=['GET'])
def get_users():
    all_users = User.query.all()
    return jsonify([user.to_dict() for user in all_users])


@user_routes.route('/users', methods=['POST'])
def add_user():
    data = request.json
    new_user = User(username=data['username'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict()), 201


blog_routes = Blueprint('blog_routes', __name__)

@blog_routes.route('/blogs', methods=['GET'])
def get_blogs():
    all_blogs = Blog.query.all()
    return jsonify([blog.to_dict() for blog in all_blogs])

@blog_routes.route('/blogs', methods=['POST'])
def add_blog():
    data = request.json
    new_blog = Blog(title=data['title'], author_id=data['author_id'], content=data['content'])
    db.session.add(new_blog)
    db.session.commit()
    return jsonify(new_blog.to_dict()), 201

@blog_routes.route('/blogs/<int:blog_id>', methods=['PUT'])
def update_blog(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    data = request.json
    blog.title = data['title']
    blog.author_id = data['author_id']
    blog.content = data['content']
    db.session.commit()
    return jsonify(blog.to_dict())

@blog_routes.route('/blogs/<int:blog_id>', methods=['DELETE'])
def delete_blog(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    db.session.delete(blog)
    db.session.commit()
    return '', 204
