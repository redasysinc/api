
import uuid

from flask import session

from models.blog import Blog
from models.post import Post
from src.common.database import Database


class User(object):
    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    @classmethod
    def get_by_id(cls, id):
        data=Database.find_one("users", {"_id":id})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_email(cls, email):
        data=Database.find_one("users", {"email": email})
        if data is not None:
            return cls(**data)

    @staticmethod
    def validate(email, password):
        user = User.get_by_email(email)
        print('user', user.email, user.password)
        if user is not None:
            return user.password == password
        print('usernot found')
        return False

    @classmethod
    def register(cls, email, password):
        user = cls.get_by_email(email)
        if user is None:
            new_user = User(email, password)
            new_user.save()
            session['email'] = email
            return True
        else:
            return False


    def login(self):
        #validate has been called already
        session['email']=self.email

    @staticmethod
    def logout():
        session['email'] = None

    def get_blogs(self):
        print('self id', self._id)
        blogs = Blog.blogs_by_author(self._id)
        print(blogs)
        return blogs
    
    def new_blog(self, title, description):
        blog=Blog(author=self._id,
                  title=title,
                  description=description)
        blog.save()

    @staticmethod
    def new_post(blog_id, title, content):
        blog = Blog.fetch(blog_id)
        blog.new_post(title=title,content=content)
    

    def json(self):
        return {
            "_id": self._id,
            "email": self.email,
            "password": self.password
        }

    def save(self):
        Database.insert("users", self.json())