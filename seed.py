from app import app
from models import db, User

with app.app_context():
    db.drop_all()
    db.create_all()   