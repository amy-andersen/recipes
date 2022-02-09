from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash #for flash messages

class Recipe:
    db_name = "recipes"

    def __init__( self , data):
        self.id = data['id']
        self.name = data['name']
        self.under_30_min = data['under_30_min']
        self.description = data['description']
        self.instructions = data['instructions']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

#insert a new recipe to db
    @classmethod
    def save(cls, data):
        query = "INSERT INTO recipes (name, under_30_min , description , instructions , user_id , created_at) VALUES (%(name)s, %(under_30_min)s, %(description)s, %(instructions)s, %(user_id)s, %(created_at)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

#get all recipes from db
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes;"
#call the connectToMySQL function with the target schema
        results = connectToMySQL(cls.db_name).query_db(query)
# Create an empty list to append instances of recipes
        recipes = []
# Iterate over the db results and create instances of recipes
        for db_row in results:
            recipes.append( cls(db_row) )
        return recipes

#get one recipe from db
    @classmethod
    def get_one_recipe(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return cls(results[0])

#edit a recipe
    @classmethod
    def update(cls,data):
        query = "UPDATE recipes SET name=%(name)s,under_30_min=%(under_30_min)s,description=%(description)s, instructions=%(instructions)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

#delete a recipe from db
    @classmethod
    def destroy(cls,data):
        query  = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

#validate recipe
    @staticmethod
    def validate_recipe(data):
        db_name = "recipes" #can't access cls variables, have to redo
        is_valid = True
        if len(data["name"]) < 3: # Must be at least 3 characters long
            is_valid = False
            flash("Name must be at least 3 characters.","recipe")
        if len(data["description"]) < 3: # Must be at least 3 characters long
            is_valid = False
            flash("Description must be at least 3 characters.","recipe")
        if len(data["instructions"]) < 3: # Must be at least 3 characters long
            is_valid = False
            flash("Instructions must be at least 3 characters.","recipe")
        if data["created_at"] == "": 
            is_valid = False
            flash("Please enter a date.","recipe") #Must be filled out
        # if data["under_30_min"] == "": 
        #     is_valid = False
        #     flash("Please specify if recipe is under 30 minutes.","recipe") #Must be filled out
        return is_valid # Return true if valid, false if not
