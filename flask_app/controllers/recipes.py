from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models.user import User
from flask_app.models.recipe import Recipe

@app.route("/create_recipe")
def create_recipe():
    if "user_id" not in session:
        return redirect('/')
    data = {
        "id" : session['user_id']
    }
    return render_template("create_recipe.html", user = User.get_one(data))

@app.route("/view_recipe/<int:id>")
def view_recipe(id):
    if "user_id" not in session:
        return redirect('/')
    data = {
        "id" : session['user_id']
    }
    recipe = {
        "id": id
    }
    return render_template("view_recipe.html", user = User.get_one(data), recipe = Recipe.get_one(recipe))

@app.route('/add_recipe', methods=["POST"])
def add_recipe():
    if not Recipe.validate_recipe(request.form):
        return redirect('/create_recipe')
    
    data = {
        "name": request.form['name'],
        "description": request.form['description'],
        "instructions": request.form['instructions'],
        "under30min": request.form['under30min'],
        "date": request.form['date'],
        "user_id": session['user_id']
    }
    Recipe.save(data)
    return redirect('/recipes')


@app.route('/delete_recipe/<int:id>')
def delete_recipe(id):
    Recipe.delete(id)
    return redirect('/recipes')

@app.route('/edit_recipe/<int:id>')
def edit_recipe(id):
    if "user_id" not in session:
        return redirect('/')
    data = {
        "id" : id
    }
    return render_template("edit_recipe.html", recipe = Recipe.get_one(data))

@app.route('/update_recipe/<int:id>', methods=["POST"])
def update_recipe(id):
    if not Recipe.validate_recipe(request.form):
        return redirect('/edit_recipe')
    
    data = {
        "id" : id,
        "name": request.form['name'],
        "description": request.form['description'],
        "instructions": request.form['instructions'],
        "under30min": request.form['under30min'],
        "date": request.form['date'],
        "user_id": session['user_id']
    }
    Recipe.update(data)
    return redirect('/recipes')