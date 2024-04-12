from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from . import db
import os
from .models import Course, CourseContent

views = Blueprint('views', __name__)


@views.route('/')
@login_required
def home_page():
    return render_template("index.html", user=current_user)


@views.route('/payment')
def payment():
    if current_user.is_authenticated:
        return render_template('payment.html', user=current_user)
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
        all_courses = Course.query.all()
        course_details = ''
        for course in all_courses:
            course_id = course.id
            course_details = CourseContent.query.filter_by(course_id=course_id).first()
            if course_details:
                course_details = course_details.course_content
            else:
                course_details = ''
        return render_template('all_courses.html', user=current_user, all_courses=all_courses,course_details=course_details)
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
            db.session.add(new_course)
            db.session.commit()
            course_id = new_course.id
            flash("New course added!", category='success')
            with open(f"src/website/templates/course_{course_id}.html","w") as f:
                with open('src/website/templates/course_base.html') as f1:
                    course_content = f1.read()
                    f.write(f"{course_content}")
            return redirect(url_for('views.all_courses'))
        
    if current_user.is_authenticated:
        all_courses = Course.query.all()
        return render_template('manage_courses.html', user=current_user, all_courses=all_courses)
    else:
        flash('Please login to see this page.', category='error')
        return redirect(url_for('auth.login'))
    

@views.route('/course_<int:course_id>')
def open_course_page(course_id):
    course_item = Course.query.filter_by(id=course_id).first()
    course_name = course_item.course_name
    instructor_name = course_item.instructor_name
    price = course_item.price
    imagfile = course_item.imagfile
    course_details = CourseContent.query.filter_by(course_id=course_id).first()
    if not course_details:
        course_details = ''
    else:
        course_details = course_details.course_content
    return render_template(f'course_{course_id}.html', user=current_user, title=course_name, instructor_name=instructor_name, price=price, imagfile=imagfile,course_details=course_details)
    

@views.route('/clicked', methods=['GET'])
def delete_course():
    course_id = request.args.get('course_id')
    if course_id:
        course_item = Course.query.filter_by(id=course_id).first()
        db.session.delete(course_item)
        db.session.commit()
        os.remove(f'src/website/templates/course_{course_id}.html')
        course_post = CourseContent.query.filter_by(course_id=course_id).all()
        for course in course_post:
            db.session.delete(course)
        db.session.commit()
    return redirect('/manage_courses#delete_bttn')


@views.route('/course_add_content', methods=['POST', 'GET'])
def course_add_content():
    course_id = request.args.get('course_id')
    if request.method == 'POST':
        course_details = request.form.get("course_details")
        course_post_old = CourseContent.query.filter_by(course_id=course_id).all()
        if course_post_old:
            for course in course_post_old:
                db.session.delete(course)
        course_post = CourseContent(course_id=course_id, course_content=course_details)
        db.session.add(course_post)
        db.session.commit()
        flash('Course content added', category='success')
        return redirect(f'/course_{course_id}')
    return render_template('course_add_content.html',user=current_user,course_details=CourseContent.query.order_by(CourseContent.course_id.desc()).first().course_content if CourseContent.query.order_by(CourseContent.course_id.desc()).first() else '')

   