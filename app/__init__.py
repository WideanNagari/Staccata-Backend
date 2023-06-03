from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import torch

app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={
    r"/*":{
        "origins": "*"
    }
})
UPLOAD_FOLDER = 'app\\temp'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config.from_object(Config)
db = SQLAlchemy(app)
Migrate = Migrate(app, db)

jwt = JWTManager(app)

from app.model import faq, reports, users, performances
from app import routes