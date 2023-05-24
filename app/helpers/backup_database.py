from app.models import Users, db, Recipes, RecipeLikes
import json
import datetime

def backup_all():
    def start_backup_wrapper(func,name):
        print("started backup " + name)
        func()
        print("finished backup " + name)
    
    start_backup_wrapper(backup_recipes,"recipes")
    start_backup_wrapper(backup_users,"users")
    start_backup_wrapper(backup_recipe_likes,"recipe_likes")


def backup_helper(filename,data):
    time_string = datetime.datetime.now().strftime("%Y %m%d H%HM%M")
    json_object = json.dumps(data)
    with open(f"data_backups/{filename} "+time_string+".json","w") as f:
        f.write(json_object)

def backup_recipe_likes():
    all_recipe_likes = RecipeLikes.query.all()
    data = []
    for recipe_like in all_recipe_likes:
        data.append(recipe_like.to_dict())
    backup_helper("recipelikes",data)
    

def backup_recipes():
    all_recipes = Recipes.query.all()
    data = []
    for recipe in all_recipes:
        data.append(recipe.to_dict())
    backup_helper("recipes",data)

def backup_users():
    all_users = Users.query.all()
    data = []
    for user in all_users:
        d = user.complete_to_dict()
        d['date_joined'] = d['date_joined'].strftime("%Y %m%d H%HM%M")
        data.append(d)
    backup_helper("users",data)

