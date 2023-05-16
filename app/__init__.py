from app.auth.auth_routes import auth
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

from . import routes
from . import models