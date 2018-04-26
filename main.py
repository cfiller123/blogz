from flask import Flask, request, redirect, render_template, flash, session
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

    def __init__(self, title, body, owner):
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

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        existing_user = User.query.filter_by(username=username).first()
        if (not username) or (not password) or (not verify):
            flash('One or more fields are empty', 'error')
        elif len(password)<3:
            flash('Password too short', 'error')
        elif len(username)<3:
            flash('Username too short', 'error')
        elif password != verify:
            flash('Passwords do not match', 'error')
        elif not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['user'] = username
            return redirect('/')
        else:
            flash('This user already exists', 'error')
    return render_template('signup.html')

@app.before_request
def require_login():
    allowed_routes = ['login', 'index', 'signup', 'blog']
    if request.endpoint not in allowed_routes and 'user' not in session:
        return redirect('/login')

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['user'] = username
            flash("Logged in")
            return redirect('/')
        elif (not user) and password:
            flash('Username incorrect or does not exist', 'error')
        elif (not password) and username:
            flash('Password incorrect', 'error')
        else:
            flash('You must enter a password and username', 'error')
    return render_template('login.html')


@app.route('/newpost', methods=['POST','GET'])
def newpost():
    if request.method == 'POST':
        blog_title = request.form['title']
        blog_content = request.form['content']
        session_user = User.query.filter_by(username=session['user']).first()
        if (not blog_title) or (not blog_content):
            flash('Please enter a title and content', 'error')
            return render_template('newpost.html', original_title=blog_title, original_content=blog_content)
        else:
            new_blog_post = Blog(blog_title,blog_content,session_user)
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
    #authorblogs = Blog.query.join(User.username).all()
    #author = authorblogs
    userID = request.args.get("user")
    if id:
        specificblog = Blog.query.filter_by(id=id).first()
        specifictitle = specificblog.title
        specificbody = specificblog.body
        #need to put username in userID
        return render_template('blog.html', specificblog_title=specifictitle, specificblog_post=specificbody, userID=userID)
    if userID:
        userblogs = Blog.query.join(User).filter_by(username=userID).all()
        return render_template('blog.html', title=userID, blogs=userblogs, userID=userID)
    #need to put username in userID
    return render_template('blog.html', title='Build A Blog', title2='Build A Blog', blogs=blogs, userID=userID)

@app.route('/logout')
def logout():
    del session['user']
    return redirect('/')

@app.route('/')
def index():
    users = ['']
    usernames = User.query.all()
    for user in usernames:
        users.append(user.username)
    return render_template('index.html', users=users)

if __name__ == '__main__':
    app.run()