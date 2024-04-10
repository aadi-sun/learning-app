from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user


views = Blueprint('views', __name__)
@views.route('/')
@login_required
def home_page():
    return render_template("index.html", user=current_user)

@views.route('/course1')
def course1():
    if current_user.is_authenticated:
        return render_template('course1.html', user=current_user)
    else:
        flash('Please login to see this page', category='error')
        return redirect(url_for('auth.login'))

@views.route('/course2')
def course2():
    if current_user.is_authenticated:
        return render_template('course2.html', user=current_user)
    else:
        flash('Please login to see this page', category='error')
        return redirect(url_for('auth.login'))

@views.route('/course3')
def course3():
    if current_user.is_authenticated:
        return render_template('course3.html', user=current_user)
    else:
        flash('Please login to see this page', category='error')
        return redirect(url_for('auth.login'))

@views.route('/course4')
def course4():
    if current_user.is_authenticated:
        return render_template('course4.html', user=current_user)
    else:
        flash('Please login to see this page', category='error')
        return redirect(url_for('auth.login'))

@views.route('/course5')
def course5():
    if current_user.is_authenticated:
        return render_template('course5.html', user=current_user)
    else:
        flash('Please login to see this page', category='error')
        return redirect(url_for('auth.login'))

@views.route('/payment')
def payment():
    if current_user.is_authenticated:
        return render_template('payment.html', user=current_user)
    else:
        flash('Please login to see this page', category='error')
        return redirect(url_for('auth.login'))

@views.route('/section1')
def section1():
    if current_user.is_authenticated:
        return render_template('section1.html', user=current_user)
    else:
        flash('Please login to see this page', category='error')
        return redirect(url_for('auth.login'))

@views.route('/section2')
def section2():
    if current_user.is_authenticated:
        return render_template('section2.html', user=current_user)
    else:
        flash('Please login to see this page', category='error')
        return redirect(url_for('auth.login'))

@views.route('/section3')
def section3():
    if current_user.is_authenticated:
        return render_template('scetion3.html', user=current_user)
    else:
        flash('Please login to see this page', category='error')
        return redirect(url_for('auth.login'))
    

@views.route('/cart')
def cart():
    if current_user.is_authenticated:
        return render_template('cart.html', user=current_user)
    else:
        flash('Please login to see this page', category='error')
        return redirect(url_for('auth.login'))
    
@views.route('/manage_courses')
def manage_courses():
    if current_user.is_authenticated and current_user.accounttype == "2":
        return render_template('manage_courses.html', user=current_user)
    else:
        flash('Please login as an instructor to see this page.', category='error')
        return redirect(url_for('auth.login'))
    