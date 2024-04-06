from flask import Blueprint, render_template
views = Blueprint('views', __name__)
@views.route('/')
def home_page():
    return render_template("index.html")

@views.route('/course1')
def course1():
    return render_template('course1.html')

@views.route('/course2')
def course2():
    return render_template('course2.html')

@views.route('/course3')
def course3():
    return render_template('course3.html')

@views.route('/course4')
def course4():
    return render_template('course4.html')

@views.route('/course5')
def course5():
    return render_template('course5.html')

@views.route('/payment')
def payment():
    return render_template('payment.html')

@views.route('/section1')
def section1():
    return render_template('section1.html')

@views.route('/section2')
def section2():
    return render_template('section2.html')

@views.route('/section3')
def section3():
    return render_template('section3.html')

@views.route('/cart')
def cart():
    return render_template('cart.html')