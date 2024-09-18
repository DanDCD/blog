from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"

    id: int = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(db.String(50), nullable=False, unique=True)
    password: str = db.Column(db.String(100), nullable=False)
    blogs = db.relationship("Blog", backref="author", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "blogs": [blog.to_dict() for blog in self.blogs],
        }


class Blog(db.Model):
    __tablename__ = "blog"

    id: int = db.Column(db.Integer, primary_key=True)
    author_id: int = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    title: str = db.Column(db.String(100), nullable=False)
    content: str = db.Column(db.Text, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "author_id": self.author_id,
            "title": self.title,
            "content": self.content,
        }
