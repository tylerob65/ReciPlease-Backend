from app.models import Recipes, Users, db, RecipeLikes
from app.auth.auth_helpers import basic_auth, token_auth
from app.api_helpers import API_Calls
from flask import Blueprint, request
from sqlalchemy import func as sql_func
from math import ceil
from sqlalchemy import desc as sql_desc

user_recipe_blueprint = Blueprint('user_recipe_blueprint',__name__)

@user_recipe_blueprint.post('/addrecipe')
@token_auth.login_required
def add_recipe():
    data = request.json
    recipe_title = data["recipe_title"]
    image_url = data['image_url']
    source_url = data['source_url']
    servings = data['servings']
    cook_time = data['cook_time']
    ingredients = data['ingredients']
    instructions = data['instructions']
    owner_id = token_auth.current_user().id

    new_recipe = Recipes(owner_id,recipe_title,instructions,ingredients,image_url,source_url,servings,cook_time)
    new_recipe.saveToDB()
    return {
        'status':'ok',
        'message':'successfully added recipe',
        'severity':'success',
        'data':{
            'recipe_id':new_recipe.id,
        },
    }, 200

@user_recipe_blueprint.route('/viewrecipe/<int:recipe_id>')
def get_recipe_for_view(recipe_id):
    recipe = Recipes.query.get(recipe_id)
    print(recipe)
    print(recipe.to_dict())

    if not recipe:
        return {
            "status":"not ok",
            "message":"Recipe ID does not exist",
            "severity":"error",
        }, 400
    
    return {
        'status':'ok',
        'message':'successfully added recipe',
        'severity':'success',
        'recipeInfo':recipe.to_dict(show_owner_username=True),
    }, 200
    
@user_recipe_blueprint.route('/editrecipe/<int:recipe_id>')
@token_auth.login_required
def get_recipe_for_modify(recipe_id):
    recipe = Recipes.query.get(recipe_id)

    if not recipe:
        return {
            "status":"not ok",
            "message":"Recipe ID does not exist",
            "severity":"error",
        }, 400


    if token_auth.current_user().id != recipe.owner_id:
        return {
            "status":"not ok",
            "message":"You do not own this recipe",
            "severity":"error",
        }, 400
    
    return {
        'status':'ok',
        'message':'Found recipe info',
        'severity':'success',
        'recipeInfo':recipe.to_dict(),
    }, 200
    

@user_recipe_blueprint.post('/updaterecipe')
@token_auth.login_required
def modify_recipe():
    data = request.json
    recipe = Recipes.query.get(data['recipeID'])
    if not recipe:
        return {
            "status":"not ok",
            "message":"This recipe does not exist",
            "severity":"error",
        }, 400
    
    print(token_auth.current_user().id)
    print("recipe owner id",recipe.owner_id)

    if token_auth.current_user().id != recipe.owner_id:
        return {
            "status":"not ok",
            "message":"You do not own this recipe",
            "severity":"error",
        }, 400
    
    recipe.title = data["recipe_title"]
    recipe.instructions = data["instructions"]
    recipe.ingredients = data["ingredients"]
    recipe.image_url = data["image_url"]
    recipe.source_url = data["source_url"]
    recipe.servings = data["servings"]
    recipe.cook_time = data["cook_time"]
    recipe.saveToDB()
    
    return {
        'status':'ok',
        'message':'Found recipe info',
        'severity':'success',
        # 'recipeInfo':recipe.to_dict(),
    }, 200
    
@user_recipe_blueprint.route('/getallrecipes')
def get_all_recipes():
    # recipe_list = Recipes.query.all()
    # db.session
    # recipe_dict
    all_recipes_query = db.select(Recipes).order_by(Recipes.id)
    all_recipes = db.session.execute(all_recipes_query).all()
    # recipe_dict = {}
    # for recipe in all_recipes:
    #     recipe_as_dict = recipe[0].shallow_to_dict(show_owner_username=True)
    #     recipe_num = recipe_as_dict['id']
    #     recipe_dict[recipe_num] = recipe_as_dict
    recipe_list = []
    for recipe in all_recipes:
        recipe_as_dict = recipe[0].shallow_to_dict(show_owner_username=True)
        recipe_list.append(recipe_as_dict)
    return {
        'status':'ok',
        'message':'Got All Recipe Info',
        'severity':'success',
        'data':recipe_list,
    }, 200


    
@user_recipe_blueprint.route('/getuserrecipes')
@token_auth.login_required
def get_user_recipes():
    user_id = token_auth.current_user().id
    user_recipes_query = db.select(Recipes).where(Recipes.owner_id==user_id).order_by(Recipes.id)
    user_recipes = db.session.execute(user_recipes_query).all()
    recipe_list = []
    for recipe in user_recipes:
        recipe_as_dict = recipe[0].shallow_to_dict(show_owner_username=True)
        recipe_as_dict["like_count"] = len(recipe[0].recipe_likers)
        recipe_list.append(recipe_as_dict)
    return {
        'status':'ok',
        'message':'Got All Recipe Info',
        'severity':'success',
        'data':recipe_list,
    }, 200


@user_recipe_blueprint.route('/gettoprecipes/<int:recipe_page>')
def get_top_recipes(recipe_page):
    
    total_recipes_stm = db.select(sql_func.count(Recipes.id))
    
    total_recipes = db.session.execute(total_recipes_stm).first()[0]
    recipes_per_page = 5
    limit = 5
    offset = (recipe_page - 1) * recipes_per_page
    max_page = ceil(total_recipes/recipes_per_page)

    query = db.session.query(
        Recipes.id,
        Recipes.title,
        Users.username,
        Recipes.owner_id,
        sql_func.count(RecipeLikes.recipe_id).label('like_count'))
    query = query.join(Users, Recipes.owner_id == Users.id)
    query = query.outerjoin(RecipeLikes, Recipes.id == RecipeLikes.recipe_id)
    query = query.group_by(Recipes.id, Users.username)
    query = query.order_by(sql_desc('like_count'),sql_desc(Recipes.date_added))
    query = query.limit(limit).offset(offset)
    results = query.all()

    recipe_list = []

    for item in results:
        recipe_list.append({
            "recipe_id":item[0],
            "recipe_title":item[1],
            "owner_username":item[2],
            "owner_id":item[3],
            "like_count":item[4],
        })
    
    data = {
        "recipe_page":recipe_page,
        "max_pages":max_page,
        "recipe_list":recipe_list,
    }

    return {
        'status':'ok',
        'message':'Got All Recipe Info',
        'severity':'success',
        'data':data,
    }, 200
    
    print(total_recipes_stm)
    print(total_recipes)
    # # CODE BELOW COUNTS THE AMOUNT OF RECIPES
    # stm = db.select(sql_func.count(Recipes.id))
    # print(stm)
    # outcome = db.session.execute(stm).first()[0]

    return {"total_pages":total_recipes}

@user_recipe_blueprint.route('/getnutritionalinfo/<int:recipe_id>')
def get_nutritional_info(recipe_id):
    recipe = Recipes.query.get(recipe_id)
    # Check if already have nutritional_info and send over if I do
    if recipe.nutritional_info:
        return {
            'status':'ok',
            'message':'Got nutritional info',
            'severity':'success',
            'data':recipe.nutritional_info
            }, 200
    
    if recipe.spoonacular_id:
        response = API_Calls.get_nutrition_spoonacular(recipe.spoonacular_id)
        nutrients = response["nutrients"]
    else:
        response = API_Calls.get_analyze_user_recipe(
            recipe.title,
            recipe.ingredients,
            recipe.instructions,
            recipe.servings,
            include_nutrition=True
        )
        nutrients = response["nutrition"]["nutrients"]
    nutritional_info = {
        "primary":{},
        "secondary":{},
    }
    for nutrient in nutrients:
        name = nutrient["name"]
        info = {
            "amount":nutrient["amount"],
            "unit":nutrient["unit"],
            "percentOfDailyNeeds":nutrient["percentOfDailyNeeds"],
        }
        
        primary_set = set([
            "Cholesterol",
            "Fat",
            "Fiber",
            "Net Carbohydrates",
            "Protein",
            "Sodium",
            "Sugar",
        ])

        if name == "Calories":
            nutritional_info["Calories"] = info
        elif name == "Carbohydrates":
            nutritional_info["primary"]["Carbs"] = info
        elif name in primary_set:
            nutritional_info["primary"][name] = info
        else: 
            nutritional_info["secondary"][name] = info
    
    print(nutritional_info)
    
    # Re-enable this when done testing
    recipe.nutritional_info = nutritional_info
    recipe.saveToDB()
    return {
        'status':'ok',
        'message':'Got All Recipe Info',
        'severity':'success',
        'data':nutritional_info
        }, 200

    
    
    
    



        
    return recipe.nutritional_info
    
    return {"didnt find nutritional info":"didn't"}
