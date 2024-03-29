from flask import Blueprint, render_template
views = Blueprint('views', __name__)
@views.route('/')
def home_page():
    return "<h1>This is the home page of the website</h1>"