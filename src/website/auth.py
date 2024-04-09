from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, logout_user, current_user, login_required

auth = Blueprint('auth', __name__)

@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password1')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                flash('Logged in successfully!', category='success')
                return redirect(url_for('views.home_page'))
            else:
                flash('Incorrect password! Try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signup',methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Account already exists.', category='error')
        elif len(email) < 4:
            flash("Email must be greater than 4 characters", category='error')
        elif len(name) < 2:
            flash("Name must be greater than 2 characters", category='error')
        elif password1 != password2:
            flash("Passwords should match", category='error')
        elif len(password1) < 7:
            flash("Length of a password must be greater than or equal to 8 characters", category='error')
        else:
            #add user to database
            new_user = User(email=email, password=generate_password_hash(password1, method='pbkdf2:sha256'), name=name)
            db.session.add(new_user)
            db.session.commit()
            flash("Account created!", category='success')
            return redirect(url_for('views.home_page'))
        
    return render_template("signup.html", user=current_user)