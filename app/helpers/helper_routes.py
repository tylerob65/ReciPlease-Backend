from app.models import Users, db, Recipes, RecipeLikes
from app.auth.auth_helpers import basic_auth, token_auth
from app.models import Recipes
from flask import Blueprint, request
from app.helpers.backup_database import backup_all
import json
import datetime
import requests
import os

RAPID_API_KEY = os.environ.get('RAPID_API_KEY')
RAPID_API_HOST = os.environ.get('RAPID_API_HOST')

helpers = Blueprint('helpers',__name__)


@helpers.route("/backupall")
def backup_all_route():
    backup_all()
    
    return {"success":"success"}

@helpers.route("/test9")
def test_recipe_likes_backup():
    all_recipe_likes = RecipeLikes.query.all()
    output = []
    for recipe_like in all_recipe_likes:
        output.append(recipe_like.to_dict())

    print(output)

    return output

@helpers.route("/test8")
def sql_test():
    # Get a person's recipe likes
    pass

@helpers.route("/test7")
def rapid_api_test():
    url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/complexSearch"

    querystring = {"query":"pasta","cuisine":"italian","excludeCuisine":"greek","diet":"vegetarian","intolerances":"gluten","equipment":"pan","includeIngredients":"tomato,cheese","excludeIngredients":"eggs","type":"main course","instructionsRequired":"true","fillIngredients":"false","addRecipeInformation":"false","titleMatch":"Crock Pot","maxReadyTime":"20","ignorePantry":"true","sort":"calories","sortDirection":"asc","minCarbs":"10","maxCarbs":"100","minProtein":"10","maxProtein":"100","minCalories":"50","maxCalories":"800","minFat":"10","maxFat":"100","minAlcohol":"0","maxAlcohol":"100","minCaffeine":"0","maxCaffeine":"100","minCopper":"0","maxCopper":"100","minCalcium":"0","maxCalcium":"100","minCholine":"0","maxCholine":"100","minCholesterol":"0","maxCholesterol":"100","minFluoride":"0","maxFluoride":"100","minSaturatedFat":"0","maxSaturatedFat":"100","minVitaminA":"0","maxVitaminA":"100","minVitaminC":"0","maxVitaminC":"100","minVitaminD":"0","maxVitaminD":"100","minVitaminE":"0","maxVitaminE":"100","minVitaminK":"0","maxVitaminK":"100","minVitaminB1":"0","maxVitaminB1":"100","minVitaminB2":"0","maxVitaminB2":"100","minVitaminB5":"0","maxVitaminB5":"100","minVitaminB3":"0","maxVitaminB3":"100","minVitaminB6":"0","maxVitaminB6":"100","minVitaminB12":"0","maxVitaminB12":"100","minFiber":"0","maxFiber":"100","minFolate":"0","maxFolate":"100","minFolicAcid":"0","maxFolicAcid":"100","minIodine":"0","maxIodine":"100","minIron":"0","maxIron":"100","minMagnesium":"0","maxMagnesium":"100","minManganese":"0","maxManganese":"100","minPhosphorus":"0","maxPhosphorus":"100","minPotassium":"0","maxPotassium":"100","minSelenium":"0","maxSelenium":"100","minSodium":"0","maxSodium":"100","minSugar":"0","maxSugar":"100","minZinc":"0","maxZinc":"100","offset":"0","number":"10","limitLicense":"false","ranking":"2"}

    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": RAPID_API_HOST,
    }

    response = requests.get(url, headers=headers, params=querystring)

    print("This is response.headers")
    # It is a special dict-like type.
    print(response.headers)

    print("This is headerdump")
    # This turns the headers into something I can send
    header_dump = json.dumps(dict(response.headers))
    print(header_dump)
    
    print("This is response.json()")
    # This is how I turn the response into a json for sending
    print(response.json())
    # return response.json()
    return header_dump

@helpers.route("/test6")
def test6_check_recipelike_relationship2():
    recipe = Recipes.query.get(3)
    print(recipe)
    recipe_likers = recipe.recipe_likers
    print(recipe_likers)
    return {"hi":"hi"}

@helpers.route("/test5")
def test5_check_recipelike_relationships1():
    user = Users.query.get(1)
    print(user)
    liked_recipes = user.liked_recipes
    print(liked_recipes)
    return {"hi":"hi"}

@helpers.route("/test4")
def test4_add_fake_like():
    new_recipe_like = RecipeLikes(6,1)
    new_recipe_like.saveToDB()
    print(new_recipe_like)
    return {"hi":"hi"}
    

@helpers.route("/test3")
def test_query_recipes_of_user():
    # Test Code query the recipes of a given user
    the_user = Users.query.get(1)
    user_recipes = the_user.user_recipes
    print(user_recipes)
    print(user_recipes[0].to_dict())


@helpers.route("/test2")
def test_query_fake_recipe():
    # Test code to query fake recipe
    the_recipe = Recipes.query.get(1)
    print(the_recipe)
    print(the_recipe.instructions)
    print(type(the_recipe.instructions))

@helpers.route("/test1")
def test_add_fake_recipe():
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
