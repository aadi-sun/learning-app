from flask import Blueprint, render_template, request
auth = Blueprint('auth', __name__)

@auth.route('/login',methods=['GET','POST'])
def login():
    data = request.form
    print(data)
    return render_template("login.html")

@auth.route('/logout')
def logout():
    return render_template("logout.html")

@auth.route('/signup',methods=['GET','POST'])
def signup():
    return render_template("signup.html")