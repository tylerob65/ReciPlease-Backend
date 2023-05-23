from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY
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

    user_recipes = db.relationship("Recipes",foreign_keys='Recipes.owner_id',back_populates="owner")
    liked_recipes = db.relationship("Recipes",secondary="recipe_likes",lazy=True)
    

    def __init__(self, username, email, password, first_name, last_name):
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
    def complete_to_dict(self):
        return {
            'id':self.id,
            'username':self.username,
            'email':self.email,
            'apitoken':self.apitoken,
            'password':self.password,
            'first_name':self.first_name,
            'last_name':self.last_name,
            'profile_pic_url':self.profile_pic_url,
            'active':self.active,
            'date_joined':self.date_joined,
        }

class Recipes(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String, nullable=False)

    date_added = db.Column(db.DateTime,nullable = False, default=datetime.utcnow())

    instructions = db.Column(ARRAY(db.String),nullable=False)
    ingredients = db.Column(ARRAY(db.String),nullable=False)
    image_url = db.Column(db.String,nullable=False)
    source_url = db.Column(db.String,nullable=False)

    servings = db.Column(db.Integer)
    cook_time = db.Column(db.Integer)
    
    owner_id = db.Column(db.Integer,db.ForeignKey(Users.id),nullable=False)
    owner = db.relationship("Users",back_populates='user_recipes',foreign_keys=[owner_id])

    recipe_likers = db.relationship("Users",secondary="recipe_likes")

    def __init__(self,owner_id,title,instructions,ingredients,image_url,source_url,servings=None,cook_time=None):
        self.owner_id = owner_id
        self.title = title
        self.instructions = instructions
        self.ingredients = ingredients
        self.image_url = image_url
        self.source_url = source_url
        self.servings = servings
        self.cook_time = cook_time

    def saveToDB(self):
        db.session.add(self)
        db.session.commit()

    def deleteFromDB(self):
        db.session.delete(self)
        db.session.commit()
    
    def to_dict(self,show_owner_username=False):
        return_dict = {
            'id':self.id,
            'owner_id':self.owner_id,
            'title':self.title,
            'instructions':self.instructions,
            'ingredients':self.ingredients,
            'image_url':self.image_url,
            'source_url':self.source_url,
            'servings':self.servings,
            'cook_time':self.cook_time,
        }

        if show_owner_username:
            return_dict["owner_username"] = Users.query.get(return_dict['owner_id']).username

        return return_dict
    
    def shallow_to_dict(self,show_owner_username=False):
        return_dict = {
            'id':self.id,
            'owner_id':self.owner_id,
            'title':self.title,
            'image_url':self.image_url,
            'source_url':self.source_url,
        }

        if show_owner_username:
            return_dict["owner_username"] = Users.query.get(return_dict['owner_id']).username

        return return_dict

class RecipeLikes(db.Model):
    __tablename__ = "recipe_likes"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    recipe_id = db.Column(db.Integer,db.ForeignKey('recipes.id'), nullable=False)
    # Item below is to make sure that person can't like recipe twice, seems to work
    __table_args__ = (db.UniqueConstraint('user_id', 'recipe_id'), )

    def __init__(self,user_id,recipe_id):
        self.user_id = user_id
        self.recipe_id=recipe_id
    
    def saveToDB(self):
        db.session.add(self)
        db.session.commit()
    
    def deleteFromDB(self):
        db.session.delete(self)
        db.session.commit()