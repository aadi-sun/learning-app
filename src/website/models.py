from . import db   
from flask_login import UserMixin



class User(db.Model, UserMixin):
    """accounttype = 1 for student and 2 for instructor"""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    name = db.Column(db.String(150))
    accounttype = db.Column(db.String(100))


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(150), unique=True)
    price = db.Column(db.Integer)
    instructor_name = db.Column(db.String(150))
    imagfile_name = db.Column(db.String(150))
    imagfile_path = db.Column(db.String(1500))


class Cartcourse(db.Model):
    """the courses which are added to favourites by all users,
      categorized based on their user_id"""
    #it is connected to Course by course id and user id 
    cart_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    course_name = db.Column(db.String(150)) 
    price = db.Column(db.Integer)
    instructor_name = db.Column(db.String(150))
    imagfile_name = db.Column(db.String(150))
    imagfile_path = db.Column(db.String(1500))

class CourseContent(db.Model):
    """the course content added by an instructor for a specific course"""
    #it is connected to Course by course_id
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    course_content = db.Column(db.String(100000))

      