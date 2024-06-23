from flask import Flask, render_template, request, session, make_response, redirect
from bson.objectid import ObjectId
from src.common.database import Database
from src.models.blog import Blog
from src.models.post import Post
from src.models.user import User

app = Flask(__name__) #name == __main__
app.secret_key = 'mysupersecretkeyshhdonttellanyone'

@app.before_request
def init_db():
    Database.initialize()

@app.route('/')
def home():
    return render_template("home.html")


@app.route('/login', methods=['GET'])
def login():
    return render_template("login.html")


@app.route('/register', methods=['GET'])
def register():
    return render_template("register.html")


@app.route('/blogs/new', methods=['POST', 'GET'])
def new_blog():
    if request.method=='GET':
        return render_template('new_blog.html')
    else:
        title=request.form['title']
        description = request.form['title']
        user = User.get_by_email(session['email'])
        author = user._id
        blog=Blog(author, title, description)
        blog.save()
        return redirect('/blogs/' + user._id)


@app.route('/blogs/delete', methods=['POST'])
def delete_blog():
    id = request.form["id"]
    Blog.delete(id)
    user = User.get_by_email(session['email'])
    return redirect('/blogs')


@app.route('/blogs/<string:user_id>')
@app.route('/blogs')
def blogs(user_id=None):
    if user_id is not None:
        user = User.get_by_id(user_id)
    else:
        user = User.get_by_email(session['email'])
    blogs = user.get_blogs()
    return render_template('user_blogs.html', blogs=blogs, email=user.email)


@app.route('/posts/<string:blog_id>')
def blog_posts(blog_id):
    print('Passed in from HTML', blog_id)
    blog=Blog.fetch(blog_id)
    posts = blog.posts()
    user = User.get_by_id(posts[0].author) if len(posts) > 0 else None
    print(posts)
    return render_template('blog_posts.html', title=blog.title, posts=posts, user=user, blogId=blog_id)


@app.route('/posts/<string:blog_id>/new', methods=['POST', 'GET'])
def new_post(blog_id):
    user = User.get_by_email(session['email'])
    blog=Blog.fetch(blog_id)
    if request.method=='GET':
        return render_template('new_post.html', title=blog.title, user=user, blogId=blog_id)
    else:
        title=request.form['title']
        content=request.form['content']
        author=request.form['author']
        blogId=request.form['blogId']
        post=Post(blogId, title, content, author)
        post.save()
        posts=blog.posts()
        return redirect('/posts/' + blog_id)


@app.route('/auth/login', methods=['POST'])
def login_user():
    email = request.form['email']
    pwd = request.form['password']
    user = User(email, pwd)
    try:
        if user.validate(email, pwd):
            user.login()
            return render_template('profile.html', email=session['email'])
        else:
            return render_template("login.html", error='Login failed for user.')
    except Exception as e:
        return render_template("login.html", error=e)



@app.route('/auth/register', methods=['POST'])
def register_user():
    email = request.form['email']
    pwd = request.form['password']
    User.register(email, pwd);
    return render_template('profile.html', email=session['email'])



if __name__ == '__main__':
    app.run()
