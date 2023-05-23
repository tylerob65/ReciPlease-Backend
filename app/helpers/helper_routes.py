from app.models import Users, db, Recipes
from app.auth.auth_helpers import basic_auth, token_auth
from app.models import Recipes
from flask import Blueprint, request
from app.helpers.backup_database import backup_all
import json
import datetime


helpers = Blueprint('helpers',__name__)


@helpers.route("/backupall")
def backup_all_route():
    backup_all()
    
    return {"success":"success"}




@helpers.route("/test1")
def test1():
    # Test code to add fake recipe
    print("Before new recipe code")
    ingredients = ["1 lb tomatoes","2 cups cheese","3 tsp sugar"]
    instructions = ["First melt the cheese","Then butter the pudding","then taste the outcome"]
    image_url = "https://images.pexels.com/photos/376464/pexels-photo-376464.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
    source_url = "foodnetwork.com/recipes/food-network-kitchen/bacon-egg-and-cheese-breakfast-burgers-5484039"
    new_recipe = Recipes(1,"Test Recipe",instructions,ingredients,image_url,source_url)
    print(new_recipe)
    print(new_recipe.to_dict())
    # new_recipe.saveToDB()
    # print("Successfully saved to db")


@helpers.route("/test2")
def test2():
    # Test code to query fake recipe
    the_recipe = Recipes.query.get(1)
    print(the_recipe)
    print(the_recipe.instructions)
    print(type(the_recipe.instructions))

@helpers.route("/test3")
def test3():
    # Test Code query the recipes of a given user
    the_user = Users.query.get(1)
    user_recipes = the_user.user_recipes
    print(user_recipes)
    print(user_recipes[0].to_dict())