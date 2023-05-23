from app.models import Recipes, Users, db
from app.auth.auth_helpers import basic_auth, token_auth
from flask import Blueprint, request

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


    
    
    # result = db.session.execute(db.select(Users).order_by(Users.id))
    # all_recipes = 
    # print(all_recipes)
    # result_first = result.first()
    # print(result_first)
    # print(type(result_first))
    # print(result_first[0])
    # print(type(result_first[0]))
    # print("results above")
    # return {"hi":all_recipes}


