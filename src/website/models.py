from . import db   
from flask_login import UserMixin

class User(db.Model, UserMixin):
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
    imagfile = db.Column(db.String(150))

class Cartcourse(db.Model):
    cart_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    course_name = db.Column(db.String(150)) 
    price = db.Column(db.Integer)
    instructor_name = db.Column(db.String(150))
    imagfile = db.Column(db.String(150))

class CourseContent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    course_content = db.Column(db.String(100000))

      