from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models.user import User
from flask_app.models.recipe import Recipe


@app.route("/")
def home():
    return render_template("new_user.html")

@app.route("/logout")
def logout():
    session.clear() #not sur why this is not working...
    return redirect("/")

@app.route("/recipes")
def recipes():
    if "user_id" not in session:
        return redirect('/')
    data = {
        "id" : session['user_id']
    }
    
    all_recipes = Recipe.get_all()
    return render_template("recipes.html", user = User.get_one(data), all_recipes = all_recipes)

@app.route('/create_user', methods=["POST"])
def create_user():
    if not User.validate_user(request.form):
        # redirect to the route where the burger form is rendered.
        return redirect('/')
    # else no errors:
    # First we make a data dictionary from our request.form coming from our template.
    # The keys in data need to line up exactly with the variables in our query string.
    data = {
        "first_name": request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email" : request.form["email"],
        "password" : bcrypt.generate_password_hash(request.form['password']),
        "pwcheck" : bcrypt.generate_password_hash(request.form['pwcheck']),
    }
    session['user_id'] = User.save(data)
    return redirect('/recipes')


@app.route('/login', methods=['POST'])
def login():
    # see if the email provided exists in the database
    data = {
        "email" : request.form["login_email"]
    }
    user_in_db = User.get_by_email(data)
    print(user_in_db)
    # user is not registered in the db
    if not user_in_db:
        flash("Invalid Email/Password", 'login')
        # print("email doesn't exist")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['login_password']):
        # if we get False after checking the password
        flash("Invalid Email/Password", "login")
        # print('password does not match')
        return redirect('/')
    # if the passwords matched, we set the user_id into session
    print('went through everything')
    session['user_id'] = user_in_db.id
    # never render on a post!!!
    return redirect("/recipes")