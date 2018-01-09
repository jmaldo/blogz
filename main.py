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
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.post_title = title
        self.post_body = body
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(150))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.pw_hash = make_pwd_hash(password)

@app.before_request
def require_login():
    allowed_routes = ['blogs_list', 'index', 'login' 'singlepost', 'userposts']
    if request.endpoint not allowed in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/', methods = ['Post', 'Get'])
def index():

    authors = User.query.all()
    return render_template('index.html', authors=authors)

@app.route('/newpost', methods=['POST', 'GET'])
def new_post():

    post_body = ''
    post_title = ''
    title_error = ''
    body_error = ''

    owner = User.query.filter_by(username=session['username']).first()

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

@app.route('/blog', methods=['Post', 'GET'])
def blogs_list():

    posts = Blog.query.all()
    users = User.query.all()
    return render_template('blog.html', posts=posts, users=users)

@app.route('singlepost', methods=['GET'])
def single_post():

    retrieved_id = request.args.get('id')
    post = Blog.query.get(retrieved_id)

    return render_template('singlepost.html', title="Single Post", post=post)

@app.route('/user-posts', methods=['Get'])
def user_posts():

    user_id = request.args.get('id')
    posts = db.session.query(Blog).filter_by(owner_id=user_id).all()

    return render_template('userpost.html', title="User Posts", post=posts)

@app.route('/login' methods=['Get', 'POST'])
def login():

    if request.method == 'Post':
        username = request.form['username']
        password = request.form['password']
        user = Usery.query.filter_by(username=usnername).first()
        if usesr and check_pw_hash(password, user.pw_hash):
            session['username'] = username
            flash("Logged In")
            return redirect(/'new-post')
        else:
            flash("User password incorrect, or user does not exist", 'error')










if __name__ == '__main__':
    app.run()