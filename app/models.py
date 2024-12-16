from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Association Table
recipe_category = db.Table(
    'recipe_category',
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipes.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id'), primary_key=True)
)

# User Model
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True, index=True)
    email = db.Column(db.String(150), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

    # Relationships
    favorites = db.relationship('Favorite', backref='user', lazy=True, cascade="all, delete-orphan")
    notes = db.relationship('Note', backref='user', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<User id={self.id} username={self.username} email={self.email} created_at={self.created_at}>'

# Recipe Model
class Recipe(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    servings = db.Column(db.Integer, nullable=False)
    prep_time = db.Column(db.Integer, nullable=False)
    cook_time = db.Column(db.Integer, nullable=False)
    
    # Relationships
    favorites = db.relationship('Favorite', backref='recipe', lazy=True, cascade="all, delete-orphan")
    notes = db.relationship('Note', backref='recipe', lazy=True, cascade="all, delete-orphan")

    # Translatable recipes data 
    translations = db.relationship('RecipeTranslation', backref='recipe', lazy=True)

    # One recipe can have multiple categories
    categories = db.relationship(
        'Category', secondary='recipe_category', backref=db.backref('recipes', lazy='dynamic')
    )

    def __repr__(self):
        return f'<Recipe id={self.id} servings={self.servings} prep_time={self.prep_time} cook_time={self.cook_time}>'


class RecipeTranslation(db.Model):
    __tablename__ = 'recipe_translations'
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)
    language = db.Column(db.String(2), nullable=False)
    name = db.Column(db.String(150), nullable=False, unique=True, index=True)
    description = db.Column(db.Text, nullable=True)
    ingredients = db.Column(db.Text, nullable=False) 
    instructions = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Recipe translation id={self.recipe_id} language={self.language} name={self.name} description={self.description} ingridients={self.ingredients} instructions={self.instructions}>'



# Category Model
class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name_en = db.Column(db.String(150), nullable=True, unique=True)
    name_ru = db.Column(db.String(150), nullable=True, unique=True)

    def __repr__(self):
        return f'<Category id={self.id} name={self.name}>'

# Favorite Model
class Favorite(db.Model):
    __tablename__ = 'favorites'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)

    def __repr__(self):
        return f'<Favorite id={self.id} user_id={self.user_id} recipe_id={self.recipe_id}>'

# Note Model
class Note(db.Model):
    __tablename__ = 'notes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) 
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False) 
    note_content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Note id={self.id} user_id={self.user_id} recipe_id={self.recipe_id}>'
