# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
# model the class after the friend table from our database
from flask import flash, session
from flask_bcrypt import Bcrypt
from flask_app.__init__ import app
from flask_app.models.user import User
bcrypt = Bcrypt(app)
import re

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.under30min = data['under30min']
        self.date = data['date']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def save(cls, data ):
        query = "INSERT INTO recipes (name , description, instructions, under30min, date, user_id, created_at, updated_at) VALUES ( %(name)s , %(description)s , %(instructions)s, %(under30min)s, %(date)s, %(user_id)s, NOW(), NOW());"
        return connectToMySQL('Recipe').query_db( query, data)
    
    @classmethod
    def update(cls, data ):
        query = "UPDATE recipes SET name = %(name)s , description = %(description)s , instructions = %(instructions)s, under30min = %(under30min)s, date = %(date)s, user_id  = %(user_id)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL('Recipe').query_db( query, data)
    
    @classmethod
    def delete(cls, recipe_id):
        query = "DELETE from recipes WHERE id = %(id)s;"
        return connectToMySQL('Recipe').query_db( query, { "id" : recipe_id} )
    
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM recipes JOIN users ON recipes.user_id = users.id WHERE recipes.id = %(id)s"
        results = connectToMySQL('Recipe').query_db(query, data)
        for row in results:
            posting_user = User({
                "id" : row["user_id"],
                "email" : row['email'],
                "first_name" : row['first_name'],
                "last_name" : row['last_name'],
                "created_at" : row['users.created_at'],
                "updated_at" : row['users.updated_at'],
                "password" : row['password']
            })
            recipe = Recipe({
                "id" : row["id"],
                "name" : row['name'],
                "description" : row['description'],
                "instructions" : row['instructions'],
                "under30min" : row['under30min'],
                "date" : row['date'],
                "created_at" : row['created_at'],
                "updated_at" : row['updated_at'],
                "user_id" : posting_user,
            })
        return recipe

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes JOIN users ON recipes.user_id = users.id ORDER BY recipes.id DESC"
        results = connectToMySQL('Recipe').query_db(query)
        all_recipes = []
        for row in results:
            posting_user = User({
                "id" : row["user_id"],
                "email" : row['email'],
                "first_name" : row['first_name'],
                "last_name" : row['last_name'],
                "created_at" : row['users.created_at'],
                "updated_at" : row['users.updated_at'],
                "password" : row['password']
            })
            new_recipe = Recipe({
                "id" : row["id"],
                "name" : row['name'],
                "description" : row['description'],
                "instructions" : row['instructions'],
                "under30min" : row['under30min'],
                "date" : row['date'],
                "created_at" : row['created_at'],
                "updated_at" : row['updated_at'],
                "user_id" : posting_user,
            })
            
            all_recipes.append(new_recipe)
        return all_recipes

    @staticmethod
    def validate_recipe(recipe):
        print(recipe)
        is_valid = True # we assume this is true
        if len(recipe['name']) < 3:
            flash("Needs 3 characters minimum", 'name')
            is_valid = False
        if len(recipe['description']) < 3:
            flash("Needs 3 characters minimum", 'description')
            is_valid = False
        if len(recipe['instructions']) < 3:
            flash("Needs 3 characters minimum", 'instructions')
            is_valid = False
        if len(recipe['date']) < 3:
            flash("Field Required", 'date')
            is_valid = False
        if 'under30min' not in recipe:
            flash("Field Required", 'under30min')
            is_valid = False
        return is_valid