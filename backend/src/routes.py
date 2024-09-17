from flask import request, jsonify, Blueprint
from src.models import Blog
from src import db

blog_routes = Blueprint('blog_routes', __name__)

@blog_routes.route('/blogs', methods=['GET'])
def get_blogs():
    all_blogs = Blog.query.all()
    return jsonify([blog.to_dict() for blog in all_blogs])

@blog_routes.route('/blogs', methods=['POST'])
def add_blog():
    data = request.json
    new_blog = Blog(title=data['title'], content=data['content'])
    db.session.add(new_blog)
    db.session.commit()
    return jsonify(new_blog.to_dict()), 201

@blog_routes.route('/blogs/<int:blog_id>', methods=['PUT'])
def update_blog(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    data = request.json
    blog.title = data['title']
    blog.content = data['content']
    db.session.commit()
    return jsonify(blog.to_dict())

@blog_routes.route('/blogs/<int:blog_id>', methods=['DELETE'])
def delete_blog(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    db.session.delete(blog)
    db.session.commit()
    return '', 204
