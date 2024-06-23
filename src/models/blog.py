import datetime
import uuid
from common.database import Database
from src.models.post import Post
from bson.objectid import ObjectId


class Blog(object):
    def __init__(self, author, title, description, _id=None):
        self.author=author
        self.title = title
        self.description = description
        self._id = uuid.uuid4().hex if _id is None else _id

    def new_post(self, title, content, date=datetime.datetime.utcnow()):
        self.content = content
        post = Post(self._id,
                    title,
                    self.content,
                    self.author,
                    date)
        post.save_to_mongo()

    def posts(self):
        print('posts', self._id)
        return Post.from_blog(self._id)

    def save(self):
        Database.insert(collection='blogs', data=self.json())

    def json(self):
        return {
            '_id': self._id,
            'author': self.author,
            'title': self.title,
            'description': self.description
        }

    @classmethod
    def fetch(cls, id):
        data = Database.find_one('blogs', {'_id': id})
        return cls(**data)
    
    @classmethod
    def blogs_by_author(cls, author):
        blogs = Database.find('blogs', {'author': str(author)})
        print(blogs)
        return [cls(**blog) for blog in blogs]

    @classmethod
    def delete(cls,  _id):
        Database.delete('blogs', _id)


