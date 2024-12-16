from flask import Flask
from .models import db
from .models import User, Recipe, RecipeTranslation, Category, Favorite, Note 



def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    db.init_app(app)
    return app