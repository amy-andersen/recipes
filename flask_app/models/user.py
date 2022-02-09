from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash #for flash messages
import re #regex module for email
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
from flask_bcrypt import Bcrypt
from flask_app import app
bcrypt = Bcrypt(app)
from flask_app.models import recipe

class User:
    db_name = "recipes"

    def __init__( self , data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

#insert a new user to db
    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(cls.db_name).query_db(query, data) # Return the ID of the new user - to be saved in session

#get data of one user
    @classmethod
    def get_one_user(cls, data):
        query = "SELECT * FROM users WHERE users.id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        user = cls(results[0])
        return user

#get data of one user with all recipes, didn't actually use this in the end.. 
    @classmethod
    def get_user_with_recipes(cls, data):
        query = "SELECT * FROM users LEFT JOIN recipes ON recipes.user_id = users.id WHERE users.id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        user = cls(results[0])
        for db_row in results:
            recipe_data = {
                "id": db_row["recipes.id"],
                "name": db_row["name"],
                "under_30_min": db_row["under_30_min"],
                "description": db_row["description"],
                "instructions": db_row["instructions"],
                "created_at": db_row["recipes.created_at"],
                "updated_at": db_row["recipes.updated_at"],
            }
        user.recipes.append( recipe.Recipe(recipe_data) )

#validate registration
    @staticmethod
    def validate_registration(data):
        db_name = "recipes" #can't access cls variables, have to redo
        is_valid = True
        if len(data["first_name"]) < 2: # Must be at least 2 characters long
            is_valid = False
            flash("First name must be at least 2 characters.","register")
        if not NAME_REGEX.match(data["first_name"]): # Must be letters only
            is_valid = False
            flash("First name must be letters only.","register")
        if len(data["last_name"]) < 2: # Must be at least 2 characters long
            is_valid = False
            flash("Last name must be at least 2 characters.","register")
        if not NAME_REGEX.match(data["last_name"]): # Must be letters only
            is_valid = False
            flash("Last name must be letters only.","register")
        if not EMAIL_REGEX.match(data['email']):
            is_valid = False
            flash("Email is invalid.","register")
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(db_name).query_db(query, data)
        if len(results) >= 1:
            is_valid = False
            flash("Email already taken.","register")
        if len(data["password"]) < 8: # Must be at least 8 characters long
            is_valid = False
            flash("Password must be at least 8 characters.","register")
        if data["password"] != data["confirm_password"]: # Passwords must match
            is_valid = False
            flash("Passwords don't match.","register")
        return is_valid # Return true if valid, false if not

#validate login, didn't use this but leave in anyways
    @staticmethod
    def validate_login(data):
        db_name = "recipes" #can't access cls variables, have to redo
        # Check that email exists in db
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(db_name).query_db(query, data)
        if len(results) == 0:
            flash("Invalid login credentials.","login")
            return False
        # Check the password
        if not bcrypt.check_password_hash(results[0]["password"], data['password']):
            flash("Invalid login credentials.","login")
            return False
        return results[0]["id"] # Return the ID of the user if their login credentials pass