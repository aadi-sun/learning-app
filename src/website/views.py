from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from . import db
import os
from .models import Course, CourseContent, Cartcourse
import random

# Creating blueprint
views = Blueprint('views', __name__)

# Defining paths of website

@views.route('/', methods=['GET', 'POST'])
@login_required
def home_page():
    # Get a random quote to display in home page
    quote = get_random_quote()
    return render_template("index.html", user=current_user, quote=quote)


@login_required
@views.route('/favourites')
def favourites():
    if current_user.accounttype == "1":
        all_fav = Cartcourse.query.all()
        all_courses_present = Course.query.all()
        return render_template("favourites.html", user=current_user, all_fav=all_fav,
                                all_courses_present=all_courses_present)
    else:
        flash('Please login to see this page', category='error')
        return redirect(url_for('auth.login'))


@login_required
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
        return render_template('all_courses.html', user=current_user, 
                               all_courses=all_courses,course_details=course_details)
    else:
        flash('Please login to see this page', category='error')
        return redirect(url_for('auth.login'))   


@login_required
@views.route('/manage_courses', methods=['GET','POST'])
def manage_courses():
    """"instructors can add courses; if the info entered is valid, 
    a course is created and an html file is created for the course"""
    if request.method == 'POST':
        #collect previous course names to see if the course has the same name as any of them
        all_courses = Course.query.all()
        course_names = [course.course_name for course in all_courses]
        course_name = request.form.get('course_name')
        instructor_name = request.form.get('instructor_name')
        price = request.form.get('price')
        imagfile = request.files['imagfile']
        #get the filename and save the image in static folder
        if imagfile:
            filename = imagfile.filename
            filepath = os.path.join('src/website/static', filename)
            imagfile.save(filepath)
            
        #display error for invalid input

        if len(course_name) < 4:
            flash('Course name should be more than 4 characters.', category='error')
        elif course_name in course_names:
            flash('A course already exists with the same name.', category='error')
        elif len(instructor_name) < 2:
            flash('Instructor name should be more than 2 characters', category='error')
        elif not imagfile:
            flash('Please include image', category='error')
        elif not price:
            flash('Please mention the price.', category='error')
        else:
            #add course to database
            new_course = Course(course_name=course_name, instructor_name=instructor_name, price=price, 
                                imagfile_name=filename, imagfile_path=filepath)
            db.session.add(new_course)
            db.session.commit()
            course_id = new_course.id
            flash("New course added!", category='success')
            #create new file for the course
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
    

@login_required
@views.route('/course_<int:course_id>')
def open_course_page(course_id):
    course_item = Course.query.filter_by(id=course_id).first()
    course_name = course_item.course_name
    instructor_name = course_item.instructor_name
    price = course_item.price
    imagfile_name = course_item.imagfile_name
    imagfile_path = course_item.imagfile_path
    course_details = CourseContent.query.filter_by(course_id=course_id).first()
    if not course_details:
        course_details = ''
    else:
        course_details = course_details.course_content
    return render_template(f'course_{course_id}.html',course_id=course_id, user=current_user, 
                           title=course_name, instructor_name=instructor_name, price=price, 
                           imagfile_name=imagfile_name, imagfile_path=imagfile_path, 
                           course_details=course_details)
    

@views.route('/clicked', methods=['GET'])
def delete_course():
    """"deletes the course, its html file and
      the course from favourites page of users"""
    course_id = request.args.get('course_id')
    if course_id:
        course_item = Course.query.filter_by(id=course_id).first()
        if course_item:

            #remove the course image from the static folder first

            imagfile_name = course_item.imagfile_name
            imagfile_path = course_item.imagfile_path
            os.remove(f'src/website/static/{imagfile_name}')

        #delete the course from the database

        db.session.delete(course_item)
        db.session.commit()

        #delete the course file

        os.remove(f'src/website/templates/course_{course_id}.html')
        course_post = CourseContent.query.filter_by(course_id=course_id).all()
        for course in course_post:
            db.session.delete(course)
        db.session.commit()

        #if someone has this course in their favourites, delete it from their favourites

        this_course_in_fav = Cartcourse.query.filter_by(course_id=course_id).all()
        for each_course in this_course_in_fav:
            db.session.delete(each_course)
            db.session.commit()

    return redirect('/manage_courses#delete_bttn')


@views.route('/delete_click')
def delete_from_fav():
    """Deletes the course from the favourites part of the database
      and then redirects it back to the favourites page"""
    course_id = request.args.get('course_id')
    if course_id:
        course_item = Cartcourse.query.filter_by(course_id=course_id, user_id=current_user.id).first()
        db.session.delete(course_item)
        db.session.commit()
    return redirect('/favourites')


@login_required
@views.route('/course_add_content', methods=['POST', 'GET'])
def course_add_content():
    """the course content should show up in the course page and
      old course content, if exists, should be deleted"""
    course_id = request.args.get('course_id')
    if request.method == 'POST':
        course_details = request.form.get("course_details")
        course_post_old = CourseContent.query.filter_by(course_id=course_id).all()
        #delete old course content
        if course_post_old:
            for course in course_post_old:
                db.session.delete(course)
        #add the new content to the database
        course_post = CourseContent(course_id=course_id, course_content=course_details)
        db.session.add(course_post)
        db.session.commit()
        flash('Course content added', category='success')
        return redirect(f'/course_{course_id}')
    return render_template('course_add_content.html',user=current_user,
                           course_details=CourseContent.query.order_by(CourseContent.course_id.desc()).first().course_content
                            if CourseContent.query.order_by(CourseContent.course_id.desc()).first() else '')

   
@views.route('/click_cart')
def add_course_to_cart():
    
    course_id = request.args.get('course_id')
    #get the course
    course = Course.query.filter_by(id=course_id).first()
    
    if course:
        #check if it is already in cart of the same person (same course)
        courses_existent = Cartcourse.query.filter_by(course_id=course_id,user_id=current_user.id).first()
        #if it is not already present, add it to the database
        if not courses_existent:
            course_name = course.course_name
            instructor_name = course.instructor_name
            price = course.price
            imagfile_name = course.imagfile_name
            imagfile_path = course.imagfile_path
            new_cart_course = Cartcourse(course_id=course_id,user_id=current_user.id, 
                                         course_name=course_name, instructor_name=instructor_name, 
                                         price=price, imagfile_name=imagfile_name, imagfile_path=imagfile_path)
            db.session.add(new_cart_course)
            db.session.commit()
            flash('Course added to favourites!!',category='success')
            all_fav = Cartcourse.query.all()
            all_courses_present = Course.query.all()
            return render_template('favourites.html',user=current_user, all_fav=all_fav, 
                                   all_courses_present=all_courses_present)
        else:
            flash('Course is already in favourites!!')
            return render_template(f'course_{ course_id }.html',user=current_user)
    return render_template('all_courses.html',user=current_user)


@login_required
@views.route('/results', methods=['POST','GET'])
def search():
    #fetch input from the user
    user = request.args.get("query")
    all_courses = Course.query.all()
    relevant_results = []
    #get all course names
    all_courses_names_list = [i.course_name for i in all_courses ]
    #if matching course is found, append it to a list
    for i in all_courses_names_list:
        if user.lower() in i.lower():
            relevant_results.append(i)
    return render_template('search_results.html',relevant_results=relevant_results, 
                           user=current_user, Course=Course)

        



# Function to get a random quote
def get_random_quote():
    quotes = [
        "The greatest glory in living lies not in never falling, but in rising every time we fall. -Nelson Mandela",
        "The way to get started is to quit talking and begin doing. -Walt Disney",
        """Your time is limited, so don't waste it living someone else's life. Don't be trapped by dogma 
        – which is living with the results of other people's thinking. -Steve Jobs""",
        "The future belongs to those who believe in the beauty of their dreams. -Eleanor Roosevelt",
        """If you look at what you have in life, you'll always have more. 
        If you look at what you don't have in life, you'll never have enough. -Oprah Winfrey""",
        """If you set your goals ridiculously high and it's a failure, 
        you will fail above everyone else's success. -James Cameron""",
        """You may say I'm a dreamer, but I'm not the only one. I hope someday you'll join us.
          And the world will live as one. -John Lennon""",
        "Education is the most powerful weapon which you can use to change the world. - Nelson Mandela",
        "Education is one thing no one can take away from you. —Elin Nordegren",
        "However difficult life may seem, there is always something you can do and succeed at. — Stephen Hawking"
]
    
    random_quote = random.choice(quotes)

    return random_quote

