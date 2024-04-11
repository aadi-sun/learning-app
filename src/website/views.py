from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from . import db
from .models import Course

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

@views.route('/all_courses')
def all_courses():
    if current_user.is_authenticated:
        return render_template('all_courses.html', user=current_user)
    else:
        flash('Please login to see this page', category='error')
        return redirect(url_for('auth.login'))   

@views.route('/manage_courses', methods=['GET','POST'])
def manage_courses():
    if request.method == 'POST':
        course_name = request.form.get('course_name')
        instructor_name = request.form.get('instructor_name')
        price = request.form.get('price')
        imagfile = request.form.get('imagfile')
        print(f"*******{course_name}*******")
        if len(course_name) < 4:
            flash('Course name should be more than 4 characters.', category='error')
        elif len(instructor_name) < 2:
            flash('Instructor name should be more than 2 characters', category='error')
        elif not imagfile:
            flash('Please include path to course image', category='error')
        elif not price:
            flash('Please mention the price.', category='error')
        else:
            #add course to database
            new_course = Course(course_name=course_name, instructor_name=instructor_name, price=price, imagfile=imagfile)
            print(new_course)
            db.session.add(new_course)
            db.session.commit()
            flash("New course added!", category='success')
            print(f"**********{new_course}**********")
            return redirect(url_for('views.all_courses'))
        
    if current_user.is_authenticated:
        return render_template('manage_courses.html', user=current_user)
    else:
        flash('Please login to see this page.', category='error')
        return redirect(url_for('auth.login'))
    
    