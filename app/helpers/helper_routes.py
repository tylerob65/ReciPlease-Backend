from app.models import Users, db, Recipes, RecipeLikes
from app.auth.auth_helpers import basic_auth, token_auth
from app.models import Recipes
from app.api_helpers import API_Calls
from flask import Blueprint, request
from app.helpers.backup_database import backup_all
import json
import datetime
import requests
import os
from sqlalchemy import func as sql_func
from sqlalchemy import desc as sql_desc


RAPID_API_KEY = os.environ.get('RAPID_API_KEY')
RAPID_API_HOST = os.environ.get('RAPID_API_HOST')

helpers = Blueprint('helpers',__name__)



@helpers.route("/backupall")
def backup_all_route():
    backup_all()
    
    return {"success":"success"}

# Reminder recipe id 23 has spoonacular id = 641907


@helpers.route("/test26")
def test_get_specific_recipe_instructions():
    with open("data_backups/recipe_test_drink.json") as f:
        recipe = json.loads(f.read())
    instructions = []
    for instruction_group in recipe["analyzedInstructions"]:
        for instruction in instruction_group["steps"]:
            instructions.append(instruction["step"])
    return instructions



@helpers.route("/test25")
def test_get_specific_recipe_info_and_save():
    recipe = API_Calls.get_recipe_info_spoonacular(659782)
    # recipe = API_Calls.get_recipe_info_spoonacular(636874)
    json_object = json.dumps(recipe)
    with open(f"data_backups/recipe_test_drink.json","w") as f:
        f.write(json_object)

    return recipe


@helpers.route("/test24")
def add_nutritional_info_to_db():
    recipe = Recipes.query.get(28)
    results = API_Calls.get_nutrition_spoonacular(recipe.spoonacular_id)
    nutritional_info = {}
    for nutrient in results["nutrients"]:
        nutritional_info[nutrient["name"]] = {
            "amount":nutrient["amount"],
            "unit":nutrient["unit"],
            "percentOfDailyNeeds":nutrient["percentOfDailyNeeds"]
        }
    recipe.nutritional_info = nutritional_info
    recipe.saveToDB()
    print(recipe.nutritional_info)
    return recipe.nutritional_info
    

@helpers.route("/test23")
def test_get_nutrient_info_from_db():
    recipe = Recipes.query.get(28)
    print(recipe.nutritional_info)
    return {"hi":"hi"}

    

@helpers.route("/test22")
def test_get_spoonacular_nutrition():
    results = API_Calls.get_nutrition_spoonacular(659782)

    new_dict = {}
    for nutrient in results["nutrients"]:
        new_dict[nutrient["name"]] = {
            "amount":nutrient["amount"],
            "unit":nutrient["unit"],
            "percentOfDailyNeeds":nutrient["percentOfDailyNeeds"]
        }
    return new_dict


    
    
    print(results)
    return results

@helpers.route("/test21")
def test_get_recipe_anaysis():
    recipe = Recipes.query.get(1)
    results = API_Calls.get_analyze_user_recipe(
        recipe.title,
        recipe.ingredients,
        recipe.instructions,
        servings = recipe.servings,
    )
    return results


@helpers.route("/test20")
def test_get_random_recipe_helper_routes():
    recipe_info = API_Calls.get_random_recipe()
    return recipe_info

@helpers.route("/test19")
def add_random_recipe_to_db():

    user_id_to_give_recipe = 1


    url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/random"
    querystring = {"number":"1"}
    headers = {
	    "X-RapidAPI-Key": RAPID_API_KEY,
	    "X-RapidAPI-Host": RAPID_API_HOST,
    }
    response = requests.get(url, headers=headers, params=querystring)
    results = response.json()
    results = results["recipes"][0]

    ingredients = [ingredient["original"] for ingredient in results["extendedIngredients"]]
    instructions = []
    for instruction in results["analyzedInstructions"][0]["steps"]:
        instructions.append(instruction["step"])
    
    recipe_info = {
        "title":results["title"],
        "image_url":results["image"],
        "source_url":results["sourceUrl"],
        "servings":results["servings"],
        "cook_time":results["readyInMinutes"],
        "owner_id":user_id_to_give_recipe,
        "ingredients":ingredients,
        "instructions":instructions,
        "spoonacular_id":results["id"]
    }
    recipe = Recipes(
        recipe_info["owner_id"],
        recipe_info["title"],
        recipe_info["instructions"],
        recipe_info["ingredients"],
        recipe_info["image_url"],
        recipe_info["source_url"],
        servings=recipe_info["servings"],
        cook_time=recipe_info["cook_time"],
        spoonacular_id= recipe_info["spoonacular_id"],
    )
    recipe.saveToDB()
    print(recipe.to_dict())
    return recipe_info

@helpers.route("/test18")
def quick_remove_recipe():
    recipe_number = 22
    recipe = Recipes.query.get(recipe_number)
    print(recipe)
    print(recipe.to_dict())
    recipe.deleteFromDB()
    return recipe.to_dict()

@helpers.route("/test17")
def test_prep_spoonacular_recipe_for_entry_into_db():
    with open("data_backups/recipe_test 2023 0527 H16M14.json") as f:
        results = json.loads(f.read())
    
    ingredients = [ingredient["original"] for ingredient in results["extendedIngredients"]]
    instructions = []
    for instruction in results["analyzedInstructions"][0]["steps"]:
        instructions.append(instruction["step"])
    
    recipe_info = {
        "title":results["title"],
        "image_url":results["image"],
        "source_url":results["sourceUrl"],
        "servings":results["servings"],
        "cook_time":results["readyInMinutes"],
        "owner_id":1,
        "ingredients":ingredients,
        "instructions":instructions,
        "spoonacular_id":results["id"]
    }

    combined_dict = {
        "original":results,
        "mine":recipe_info,
    }

    save_info = True
    if not save_info:
        return combined_dict
    
    recipe = Recipes(
        recipe_info["owner_id"],
        recipe_info["title"],
        recipe_info["instructions"],
        recipe_info["ingredients"],
        recipe_info["image_url"],
        recipe_info["source_url"],
        servings=recipe_info["servings"],
        cook_time=recipe_info["cook_time"],
        spoonacular_id= recipe_info["spoonacular_id"],
    )
    recipe.saveToDB()
    combined_dict["success"] = True
    return combined_dict

@helpers.route("/test16")
def test_store_spoonacular_recipe_and_store():
    # Note. Just given permission to store spoonacular recipes as long as I don't host
    url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/random"

    querystring = {"number":"1"}

    headers = {
	    "X-RapidAPI-Key": RAPID_API_KEY,
	    "X-RapidAPI-Host": RAPID_API_HOST,
    }

    response = requests.get(url, headers=headers, params=querystring)
    results = response.json()
    results = results["recipes"][0]
    print(results)
    print(type(results))
    json_object = json.dumps(results)
    time_string = datetime.datetime.now().strftime("%Y %m%d H%HM%M")
    with open(f"data_backups/recipe_test "+time_string+".json","w") as f:
        f.write(json_object)

    return results

@helpers.route("/test15")
def test_show_temporary_stored_recipe_json_for_use_in_formatting():

    with open("data_backups/recipe_test 2023 0525 H22M06.json") as f:
        results = json.loads(f.read())
    
    return results

@helpers.route("/test14")
def test_analyze_recipe():
    recipe = Recipes.query.get(1)
    recipe_info = recipe.to_dict()

    url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/analyze"

    querystring = {"language":"en","includeNutrition":"true","includeTaste":"false"}

    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": RAPID_API_HOST
    }

    payload = {
        "title": recipe_info["title"],
        "ingredients": recipe_info["ingredients"],
        "instructions": " ".join(recipe_info["instructions"]),
    }
    if recipe_info["servings"]:
        payload["servings"] = recipe_info["servings"]
    response = requests.post(url, json=payload, headers=headers, params=querystring)
    results = response.json()
    print(results)
    
    # print(" ".join(recipe_info["instructions"]))
    
    # print(recipe_info)

    # Create temporary backup of one recipe so I can work on formatting frontend
    # without repeated API calls
    # json_object = json.dumps(results)
    # time_string = datetime.datetime.now().strftime("%Y %m%d H%HM%M")
    # with open(f"data_backups/recipe_test "+time_string+".json","w") as f:
    #     f.write(json_object)

    



    return results
    # return {"hi":"hi"}

@helpers.route("/test13")
def test_sql_paginate3():
    
    # The following works
    query = db.session.query(
        Recipes.id,Recipes.title,
        Users.username,
        sql_func.count(RecipeLikes.recipe_id).label('like_count'))
    query = query.join(Users, Recipes.owner_id == Users.id)
    query = query.outerjoin(RecipeLikes, Recipes.id == RecipeLikes.recipe_id)
    query = query.group_by(Recipes.id, Users.username).order_by(sql_desc('like_count'),sql_desc(Recipes.date_added))
    # The items below just need to be tuned for which page to show
    query = query.limit(5).offset(10)
    query = query.all()
    # print(query)
    for item in query:
        print(item)
    return {"hi":"hi"}

@helpers.route("/test12")
def test_sql_paginate2():
    # stm = db.select(Users.id).order_by(sql_desc(Users.id))
    # print(stm)
    # result = db.session.execute(stm).all()
    # print(result)

    # stm2 = db.select(Users.id).order_by(sql_desc(Users.id)).limit(2)
    # print(stm2)
    # result = db.session.execute(stm2).all()
    # print(result)

    # stm3 = db.select(Users.id).order_by(sql_desc(Users.id)).offset(5).limit(2)
    # print(stm3)
    # result = db.session.execute(stm3).all()
    # print(result)

    # stm4 = db.select(Users.id).order_by(sql_desc(Users.id)).fetch(1)
    # print(stm4)
    # result = db.session.execute(stm4).all()
    # print(result)

    # print("new group")
    # stm = db.select(Users.id).order_by(sql_desc(Users.id))
    # print("stm")
    # print(stm)
    # sub = stm.subquery()
    # print("sub")
    # print(sub)
    # print("new sub")
    # new_sub = db.select(sql_func.count(sub))
    # print(new_sub)

    # # CODE BELOW COUNTS THE AMOUNT OF RECIPES
    # stm = db.select(sql_func.count(Recipes.id))
    # print(stm)
    # outcome = db.session.execute(stm).first()[0]
    # print(outcome)

    stm = db.select(Recipes.id,Recipes.title,Recipes.owner_id)
    print(stm)

    stm = db.select(RecipeLikes.recipe_id,sql_func.count(RecipeLikes.id).label("count"))
    stm = stm.group_by(RecipeLikes.recipe_id)
    stm = stm.order_by(sql_desc("count"))
    sub = stm.subquery()
    print(sub)
    print(db.select(sub))
    # stm = (
    #     select(Users)
        
    # )

    print(sub)
    # new_stm = db.select(Recipes.id,Recipes.title,Recipes.owner_id).label("subq")
    # j = db.join(Recipes,sub,Recipes.id==sub.c.recipe_id)
    # # stm=db.select(Recipes).select_from(j)
    # stm=db.select(Recipes.id,sub.count).select_from(j)
    # results = db.session.execute(stm).all()
    # print(results)
    # print(results[1])
    # Recipes_by_like = db.session.execute(stm)
    # print(Recipes_by_like.all())

    """
    SELECT RECIPES
    JOIN SUBQUERY ON ()
    
    
    """

    # stm = db.select(Recipes.id,Recipes.title,Recipes.owner_id)
    # print(stm)


    





    return {"hi":"hi"}

@helpers.route("/test11")
def test_sql_paginate():
    stm = db.select(RecipeLikes.recipe_id,sql_func.count(RecipeLikes.id).label("count"))
    stm = stm.group_by(RecipeLikes.recipe_id)
    stm = stm.order_by(sql_desc("count"))
    print("stm")
    print(stm)

    # 
    # Outcome - Paginate can't handle compound select
    # 

    pagination = db.paginate(stm,per_page=2)
    print("pagination")
    print(pagination)
    print("pagination.page")
    print(pagination.page)
    print("pagination.total")
    print(pagination.total)
    # print("pagination.items")
    # print(pagination.items)
    for item in pagination:
        print(item)


    return {"hi":"hi"}

@helpers.route("/test10")
def test_sql_select():
    # Selects Recipe_likes and sorts them in descending order
    stm = db.select(RecipeLikes.recipe_id,sql_func.count(RecipeLikes.id).label("count"))
    stm = stm.group_by(RecipeLikes.recipe_id)
    stm = stm.order_by(sql_desc("count"))
    print(stm)
    output = db.session.execute(stm)
    print(output)
    print(output.all())
    return {"hi":"hi"}


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
