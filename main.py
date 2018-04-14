from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:test@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(240))
    body = db.Column(db.Text)

    def __init__(self, name):
        self.title = title
        self.body = body

@app.route('/newpost', methods=['POST','GET'])
def newpost():
    if request.method == 'POST'
        blog_title = request.form['title']
        blog_content = request.form['content']
        new_blog_post = Blog(blog_title,bog_content)
        db.session.add(new_blog_post)
        db.session.commit()
        return render_template('base.html')
    else:
        return render_template('newpost.html',title=)

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('blog.html', title='Build A Blog')


if __name__ == '__main__':
app.run()