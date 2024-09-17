

class blog:
    def __init__(self, id, title, author_id, timestamp, content):
        self.id = id # the unique id of this blog
        self.title = title # the title of this blog
        self.author_id = author_id # the author of this blog
        self.timestamp = timestamp
        self.content = content

    def __repr__(self):
        return f'<Blog: {self.title}>'