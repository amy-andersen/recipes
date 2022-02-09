from flask_app import app
from flask import render_template,redirect,request,session
from flask_app.models import recipe,user

#form template to add recipe
@app.route('/recipes/new')
def add_recipe():
    if "user_id" not in session: # If not logged in send to login page
        return redirect("/")
    data = {
        "id": session["user_id"]
    }
    return render_template("add_recipe.html", this_user=user.User.get_one_user(data))

#template to view one recipe
@app.route('/recipes/<int:id>')
def view_recipe(id):
    if "user_id" not in session: # If not logged in send to login page
        return redirect("/")
    data = {
        "id": id
    }
    user_data = {
    "id": session["user_id"]
    }
    return render_template("view_recipe.html", recipe=recipe.Recipe.get_one_recipe(data), this_user=user.User.get_one_user(user_data))

#template for editing a recipe
@app.route('/recipes/edit/<int:id>')
def edit_recipe(id):
    if "user_id" not in session: # If not logged in send to login page
        return redirect("/")
    data = {
        "id": id
    }
    user_data = {
        "id": session["user_id"]
    }
    return render_template("edit_recipe.html", recipe=recipe.Recipe.get_one_recipe(data), user=user.User.get_one_user(user_data))

#post method to add recipe
@app.route('/add_recipe', methods = ["POST"])
def add():
    if "user_id" not in session: # If not logged in send to login page
        return redirect("/")
    # Validate data
    if not recipe.Recipe.validate_recipe(request.form):
        return redirect("/recipes/new") # Send user back to add recipe
    data = {
        "name": request.form["name"],
        "under_30_min": request.form["under_30_min"],
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "user_id": session["user_id"],
        "created_at": request.form["created_at"]
    }
    recipe.Recipe.save(data)
    return redirect('/dashboard')

#post method to edit recipe
@app.route('/edit/recipe/<int:id>', methods = ["POST"])
def edit(id):
    if "user_id" not in session: # If not logged in send to login page
        return redirect('/')
    # Validate data
    if not recipe.Recipe.validate_recipe(request.form):
        return redirect(f'/recipes/edit/{id}') # Send user back to edit recipe
    data = {
        "name": request.form["name"],
        "under_30_min": request.form["under_30_min"],
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "id": id
    }
    recipe.Recipe.update(data)
    return redirect('/dashboard')

#method to delete recipe
@app.route('/delete/recipe/<int:id>')
def destroy(id):
    if "user_id" not in session: # If not logged in send to login page
        return redirect("/")
    data ={
        "id": id
    }
    recipe.Recipe.destroy(data)
    return redirect('/dashboard')