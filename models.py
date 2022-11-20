from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
# from app import app 

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    """ connect to database """
    db.app = app
    db.init_app(app)

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    
    @classmethod
    def signup(cls, email, password):
        """ signup user, hashes password and adds user to database """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            email=email,
            password=hashed_pwd
        )

        db.session.add(user)
        
        return user

    @classmethod
    def login(cls, email, password):
        """ check password hash against password and logs in user """

        user = cls.query.filter_by(email=email).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False