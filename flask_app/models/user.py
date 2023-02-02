# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
# model the class after the friend table from our database
from flask import flash, session
from flask_bcrypt import Bcrypt
from flask_app.__init__ import app
bcrypt = Bcrypt(app)
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
#this only makes sure there is a something before and after @, but no ".com"

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # self.posts = []

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('Recipe').query_db(query)
        # Create an empty list to append our instances of friends
        users = []
        # Iterate over the db results and create instances of friends with cls.
        for user in results:
            users.append( cls(user) )
        return users
    
    # class method to save our friend to the database
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO users (first_name , last_name , email, password, created_at, updated_at) VALUES ( %(first_name)s , %(last_name)s , %(email)s, %(password)s, NOW(), NOW());"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('Recipe').query_db( query, data)

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        result = connectToMySQL('Recipe').query_db(query, data)
        return cls(result[0])
        #result is a list

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        result = connectToMySQL('Recipe').query_db(query, data)
        # print(result)
        if len(result) < 1:
            return False
        return cls(result[0])

    @staticmethod
    def validate_user(user):
        is_valid = True # we assume this is true
        if len(user['first_name']) < 3:
            flash("First name must be at least 3 characters.", 'first_name')
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Last name must be at least 3 characters.", 'last_name')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", 'email')
            is_valid = False
        users = User.get_all()
        for each_user in users:
                if each_user.email == user['email']:
                    flash("Email address already exists!", 'email')
                    is_valid = False
        # print(user['password'])
        # print(user['pwcheck'])
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters.", 'password')
            is_valid = False
        if not user['password'] == user['pwcheck']:
            flash("Password doesn't match.", 'pwcheck')
            is_valid = False
        
        session['first_name'] = user['first_name']
        session['last_name'] = user['last_name']
        session['email'] = user['email']
        session['password'] = user ['password']
        return is_valid