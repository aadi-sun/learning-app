from flask import Blueprint, render_template
auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template("login.html")

@auth.route('/logout')
def logout():
    return "<h1>This is the logout page</h1>"

@auth.route('/signup')
def signup():
    return "<h1>This is the signup page</h1>"