from flask_app import app
from flask import render_template,redirect,request,session
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models import user,recipe

#index page for register/login forms
@app.route('/')
def index():
    if "user_id" in session: # If logged in, send the user to home page
        return redirect("/dashboard")
    return render_template("login.html")

#template for home page
@app.route('/dashboard')
def home():
    if "user_id" not in session: # If not logged in send to login page
        return redirect("/")
    data = {
    "id": session["user_id"]
    }
    this_user = user.User.get_one_user(data)
    recipes = recipe.Recipe.get_all()
    return render_template("dashboard.html", this_user = this_user, recipes = recipes)

#post method for registration
@app.route('/register', methods=["POST"])
def add_new_user():
    # Validate data
    if not user.User.validate_registration(request.form):
        return redirect("/") # Send user back to login page
    # Create the new user
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": bcrypt.generate_password_hash(request.form['password']),
    }
    # Save new user id in session if successful and send to home page
    session["user_id"] = user.User.save(data)
    return redirect("/dashboard")

#post method for login
@app.route('/login', methods=["POST"])
def login():
    data = {
        "email": request.form["email"],
        "password": request.form["password"]
    }
    is_valid = user.User.validate_login(data)
    if is_valid == False: # Invalid input from form, send back to login page
        return redirect("/")
    else:
        session["user_id"] = is_valid # Set session variable = ID, go to home page
        return redirect("/dashboard")

#method for logout
@app.route('/logout')
def logout():
    session.clear() # Forget user_id
    return redirect("/")