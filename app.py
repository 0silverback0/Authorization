from flask import Flask, render_template, redirect, flash, session, g
from models import connect_db, db, User
from forms import Form
import os, config

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_KEY
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'key')

    with app.app_context():
        connect_db(app)
        db.create_all()
    return app

app = create_app()

CURR_USER_KEY = 'curr_user'

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None

def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id

def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@app.route('/', methods=['GET', 'POST'])
def home():
    """ render forms """
    form = Form()
    return render_template('index.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """ signup user and add to g"""
    form = Form()
    try:
        if form.validate_on_submit():    
            user = User.signup(email=form.email.data, password=form.password.data)   
            db.session.commit()
            do_login(user)
            return redirect('/loggedin')
    except:
        flash('Email Already In Use')
        return redirect('/')
    return render_template('index.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """ logs in user """
    form = Form()
    email = form.email.data
    password = form.password.data
    user = User.query.filter(User.email == email)
    try:
        if form.validate_on_submit():
            user.login(email, password)
            if user:
                do_login(user)
                flash('Welcome')
                return redirect('/loggedin')
    except:
        flash('Worng Email or Password')
        return redirect('/')
    
    return redirect('/')

@app.route('/loggedin')
def loggedin():
    """ takes loges in user to dashboard """
    flash(f'Welcome {g.user.email}')
    return render_template('loggedin.html')
    

@app.route('/logout')
def logout():
    """ logout user and redirect to home page """
    do_logout()
    flash(f'{g.user.email} has logged out')
    return redirect("/")