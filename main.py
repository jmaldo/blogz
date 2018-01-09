from flask import Flask, request, redirect, render_template, sessions, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:root@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

app.secret_key = 'thekeyofkeys'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    post_title = db.Column(db.String(120))
    post_body = db.Column(db.String(25000))
    ower_id = db.Column(db.integer, db.ForeignKey('user.id'))

    def __init__(self, title, body):
        self.post_title = title
        self.post_body = body
        self.owner = owner

@app.route('/blog', methods = ['POST','GET'])
def index():

    posts = Blog.query.all()
    return render_template('blog.html', title="Build a Blog", posts=posts)

@app.route('/newpost', methods=['POST', 'GET'])
def new_post():

    post_body = ''
    post_title = ''
    title_error = ''
    body_error = ''

    if request.method == 'POST':
        post_title = request.form['post_title']
        post_body = request.form['post_body']
        if post_title == '':
            title_error = 'Please enter a Post Title.'
        elif post_body == '':
            body_error = 'Please enter some content.'
        else:
            new = Blog(post_title, post_body)
            db.session.add(new)
            db.session.commit()

            return redirect('/singlepost?id={0}'.format(new.id))

    return render_template('newpost.html', title="New Post", title_error=title_error,
                body_error=body_error, post_title=post_title, post_body=post_body)

@app.route('/singlepost', methods=['GET'])
def single_post():

    retrieved_id = request.args.get('id')
    posts = db.session.query(Blog.post_title, Blog.post_body).filter_by(id=retrieved_id)

    return render_template('singlepost.html', title="Single Post", posts=posts)

if __name__ == '__main__':
    app.run()