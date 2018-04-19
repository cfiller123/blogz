from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'supersecretkey'

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(240))
    body = db.Column(db.Text)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owern):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog',backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.route('/signup', methods=['POST'])
def signup():

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
    if user and user.password == password:
            session['email'] = email
            flash("Logged in")
            return redirect('/')
    else:
            flash('User password incorrect, or user does not exist', 'error')

    return render_template('login.html')


@app.route('/newpost', methods=['POST','GET'])
def newpost():
    if request.method == 'POST':
        blog_title = request.form['title']
        blog_content = request.form['content']
        if (not blog_title) or (not blog_content):
            flash('Please enter a title and content', 'error')
            return render_template('newpost.html', original_title=blog_title, original_content=blog_content)
        else:
            new_blog_post = Blog(blog_title,blog_content,session['email'])
            db.session.add(new_blog_post)
            db.session.commit()
            id = str(new_blog_post.id)
            blogs = Blog.query.all()
            if (not blog_title) or (not blog_content):
                flash('Please enter a title and content', 'error')
                return render_template('newpost.html', original_title=blog_title, original_content=blog_content)
            else:
                specificblog = Blog.query.filter_by(title=blog_title).first()
                return redirect('/blog?id='+id)
    return render_template('newpost.html', title="Build A Blog")

@app.route('/blog', methods=['GET'])
def blog():
    blogs = Blog.query.all()
    id = request.args.get("id")
    if id:
        specificblog = Blog.query.filter_by(id=id).first()
        specifictitle = specificblog.title
        specificbody = specificblog.body
        return render_template('blog.html', specificblog_title=specifictitle, specificblog_post=specificbody)
    return render_template('blog.html', title='Build A Blog', title2='Build A Blog', blogs=blogs)

@app.route('/')
def index():
    return redirect('/blog')

if __name__ == '__main__':
    app.run()