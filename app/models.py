from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from secrets import token_hex
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

class Users(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),nullable = False,unique=True)
    email = db.Column(db.String(100),nullable = False,unique=True)
    apitoken = db.Column(db.String,unique=True)
    password = db.Column(db.String,nullable=False)
    first_name = db.Column(db.String(50), nullable = False)
    last_name = db.Column(db.String(50))
    profile_pic_url = db.Column(db.String)
    active = db.Column(db.Boolean,nullable=False,default=True)
    date_joined = db.Column(db.DateTime,nullable = False, default=datetime.utcnow())
    

    def __init__(self, username, email, password, first_name,last_name):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.first_name = first_name
        self.last_name = last_name
        self.apitoken = token_hex(16)

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()

    def deleteFromDB(self):
        db.session.delete(self)
        db.session.commit()
    
    def to_dict(self):
        return {
            'id':self.id,
            'username':self.username,
            'email':self.email,
            'apitoken':self.apitoken,
        }


    
    
    

