from app.auth.auth_routes import auth
from app.user_recipe_blueprint.user_recipe_blueprint_routes import user_recipe_blueprint
from app.helpers.helper_routes import helpers
from app.models import db, Users
from flask import Flask
from config import Config
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app,db)

cors = CORS(app)
cors.init_app(app)

app.register_blueprint(auth)
app.register_blueprint(user_recipe_blueprint)
app.register_blueprint(helpers)

from . import routes
from . import models