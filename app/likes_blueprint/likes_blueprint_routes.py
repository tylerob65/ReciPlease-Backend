from app.models import Recipes, Users, db, RecipeLikes
from app.auth.auth_helpers import basic_auth, token_auth
from flask import Blueprint, request

likes_blueprint = Blueprint('likes_blueprint',__name__)

@likes_blueprint.route('/doilike/<int:recipe_id>')
@token_auth.login_required
def does_user_like_recipe(recipe_id):
    user_id = token_auth.current_user().id
    # cart_entry = Carts.query.filter(db.and_(Carts.user_id==user_id,Carts.product_id==product_id)).all()

    result = RecipeLikes.query.filter(db.and_(RecipeLikes.user_id==user_id,RecipeLikes.recipe_id==recipe_id)).all()
    
    return {
            "status":"ok",
            "message":"Result of whether user likes recipe",
            "severity":"success",
            "data":{"liked":len(result)==1},
        }, 200

# @likes_blueprint.route('/likerecipe/<int:recipe_id>')
# @token_auth.login_required
# def like_recipe(recipe_id):
    user = token_auth.current_user()
    print(user)
    user_id = user.id

    # TODO double check we are sending it along as recipe_id
    result = RecipeLikes.query.filter(db.and_(RecipeLikes.user_id==user_id,RecipeLikes.recipe_id==recipe_id)).all()
    if len(result)==1:
        return {
            "status":"not ok",
            "message":"Recipe already liked",
            "severity":"error",
        }, 401
    
    new_like = RecipeLikes(user_id,recipe_id)
    new_like.saveToDB()

    return {
        "status":"ok",
        "message":"Successfully Liked Recipe",
        "severity":"success",
    }, 200

@likes_blueprint.route('/unlikerecipe/<int:recipe_id>')
@token_auth.login_required
def unlike_recipe(recipe_id):
    user = token_auth.current_user()
    print(user)
    user_id = user.id

    # TODO double check we are sending it along as recipe_id
    result = RecipeLikes.query.filter(db.and_(RecipeLikes.user_id==user_id,RecipeLikes.recipe_id==recipe_id)).all()
    if len(result)==0:
        return {
            "status":"not ok",
            "message":"Recipe wasn't already liked",
            "severity":"error",
        }, 401
    
    like_to_delete = result[0]
    like_to_delete.deleteFromDB()

    return {
        "status":"ok",
        "message":"Successfully Stopped Liking Recipe",
        "severity":"success",
    }, 200


@likes_blueprint.post('/likerecipe')
@token_auth.login_required
def like_recipe():
    print(request)
    user = token_auth.current_user()
    print(user)
    user_id = user.id
    data = request.json

    # TODO double check we are sending it along as recipe_id
    recipe_id = data["recipe_id"]
    result = RecipeLikes.query.filter(db.and_(RecipeLikes.user_id==user_id,RecipeLikes.recipe_id==recipe_id)).all()
    if len(result)==1:        
        return {
            "status":"not ok",
            "message":"Recipe already liked",
            "severity":"error",
        }, 401
    
    new_like = RecipeLikes(user_id,recipe_id)
    new_like.saveToDB()

    return {
        "status":"ok",
        "message":"Successfully Liked Recipe",
        "severity":"success",
    }, 200





    # Get recipe_id from data
    # Check if user already likes recipe
    # if does then send error message
    # If doesn't then add
    
    
    
    



