import datetime
import uuid

from src.common.database import Database


class Post(object):
    def __init__(self, blogId, title, content, author, created=datetime.datetime.utcnow(), _id=uuid.uuid4().hex):
        self.blogId = blogId
        self.title = title
        self.content = content
        self.author = author
        self.created = created
        self._id = _id

    def save(self):
        Database.insert('posts', self.json())

    def json(self):
        return {
            '_id': self._id,
            'blogId': self.blogId,
            'author': self.author,
            'content': self.content,
            'title': self.title,
            'created': self.created
        }

    @classmethod
    def fetch(cls, id):
        data = Database.find_one('posts',{'_id': id})
        return cls(**data)

    @classmethod
    def from_blog(cls, blogId):
        print('Post.from_blog', blogId)
        posts = Database.find('posts', {'blogId': blogId})
        return [cls(**post) for post in posts]
