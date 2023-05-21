from app.models import Users, db
from app.auth.auth_helpers import basic_auth, token_auth
from flask import Blueprint, request

user_recipe_blueprint = Blueprint('user_recipe_blueprint',__name__)

@user_recipe_blueprint.post('/createrecipe')
@token_auth.login_required
def create_recipe():
    data = request.json
    

    # Get data from request


