from flask import Flask, request, jsonify

app = Flask(__name__)
blogs = []  # In-memory storage for blogs



@app.route('/blogs', methods=['GET'])
def get_blogs():
    return jsonify(blogs)

@app.route('/blogs', methods=['POST'])
def add_blog():
    new_blog = request.json
    blogs.append(new_blog)
    return jsonify(new_blog), 201

@app.route('/blogs/<int:blog_id>', methods=['PUT'])
def update_blog(blog_id):
    updated_blog = request.json
    blogs[blog_id] = updated_blog
    return jsonify(updated_blog)

@app.route('/blogs/<int:blog_id>', methods=['DELETE'])
def delete_task(blog_id):
    blogs.pop(blog_id)
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
