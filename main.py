from flask import Flask, request, redirect, render_template, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:root@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

app.secret_key = 'thekeyofkeys'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.DateTime)

    def __init__(self, title, body, owner_id, date=None):
        self.title = title
        self.body = body
        self.owner_id = owner_id
        if date is None:
            date = datetime.utcnow()
        self.date = date

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(150))
    blogs = db.relationship('Blog', backref='user')

    def __init__(self, username, password):
        self.username = username
        self.pw_hash = make_pwd_hash(password)

@app.before_request
def require_login():
    allowed_routes = ['login', 'blog', 'index' 'singnup']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/')
def index():

    users = User.query.order_by(User.username).all()
    return render_template('index.html', title="Home", users = users)

@app.route('/logins', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            session['username'] = username
            flash("Logged in")
            return redirect('/newpost')
        elif user and user.password != password:
            flash('Your password is incorrect', 'error')
            return render_template('login.html', username=username)

    return render_template('login.html', title='login',)


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        existing_user = User.query.filter_by(username=username).first()
        is_error = False
        #username check
        if not username:
            flash('You need to enter a user name', 'error')
            is_error = True
        
        elif existing_user:
            flash('Username already exists', 'error')
            is_error = True

        elif len(username) < 3 or len(username) > 20 or ('' in username):
            flash('Your user= name must be between 3 and 20 caracters in length and conatin no spaces', 'error')
            is_error = True

        if not password:
            flash('You need to enter a password', 'error')
            is_error =True

        if not verify:
            flash('You need to verify your password', 'error')
            is_error = True

        elif password != verify:
            flash('Verification failed, your passwords did not match', 'error')
            is_error = True
        
        if is_error == True"
            return render_template('signup.html', username=username)

        else:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/newpost')
        return render_template('signup.html', title="signup")

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blog')

@app.route('/blog', methods=['POST', 'GET'])
def blog():

    user_username = request.args.get('user')
    blog_id = request.args.get('id')

    if blog_id:
        blog = Blog.query.get(blog_id)
        return render_template('blog.html', title="ABlog", blog=blog)
    elif user_username:
        user = User.query.filter_by(username=user_username).first()
        user_blogs = Blog.query.filter_by(owner_id=user.id).all()
        return render_template('singleuser.html', title="Userblogs", blogs=user_blogs)

    else:
        post_blogs = Blog.query.order_by(Blog.date.desc()).all()
        return render_template('singleuser.html', title="Blogz", blogs=posted_blogs)

@app.route('/newpost', methods=['GET', 'POST'])
def newpost():
    owner = User.query.filter-by(username-session['username']).first()

    if request.method == 'POST':
        new_title = request.form['title']
        new_body = request.form['body']
        new_blog = Blog(new_title,  new_body, owner_id)

        is_error = False

        if not new_title:
            flash('You need to enter a title', 'erro')
            is_error = True
        elif not new_body:
            flash('You need to enter something in your post', 'error')
            is_error = True

        if is_error == True
            return redirect('/newpost')

        if is_error == True
            return redirect('/newpost')
        else:
            db.session.add(new_blog)
            db.session.commit()
            return redirect(url_for('blog',id=str(new_blog.id)))

    return render_template('newpost.html', title = "newpost")

if __name__=='__main__':
    app.run()

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'Post':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

    # --------Blank Fields--------

    if len(username) == 0:
        flash("The User Name field was left blank.", 'error')
    else:
        username = username
    if len(password) == 0:
        flash('The Password field was left bank.', 'error')
    else: 
        password = password
    if len(verify) == 0:
        flash('The verify password field was left blank', 'error')
    else:
        verify = verify

    #---------Invalid User Name, Password, user name--------

    if len(username) !=0:
        if len(username) < 4 or len(username) > 50 or ' ' in username:
            flash('User Name must be between 4 and 20 characters long and cannot contain spaces.', 'error')
            return render_template('/signup.html')
        else: 
            username = username

        if len(password) != 0:
            if len(password) < 4 or len(password) > 150 or ' ' in password:
                flash("Password must be between 4 and 19 characters long and cannot conatin spaces.", 'error')
                return render_template('/signup.html')
        else: 
            password = password

    #--------Password and Verify Do Not Match-----------

    if len(password) == len(verify):
        for char, letter in zip(password, verify):
            if char !=letter:
                flash('Password do not match', error)
                return render_template('signup.html')
        else:
               verify = verify
               password = password
    else:
            flash('Password Do Not Match.', 'error')
            return render_template('signup.html')

    if username and password and verify:
            existing_user = User.query.filter_by(username=username).first()
            if not existing_user:
                new_user = User(username, password)
                db.session.add(new_user)
                db.session.commit()
                session['username'] = username
                return redirect('/new-post')
            else:

                flash('Duplicate User.', 'error')
    else:
            return render_template('signup.html')

    return render_template('signup.html')

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blog')


if __name__ == '__main__':
    app.run()   