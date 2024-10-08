from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import random


#create database
db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    #make and initialize app
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'bkgkrvi,si.jgikcvgestn'
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"
    app.config['UPLOAD_FOLDER'] = 'static'
    db.init_app(app)

    #import and register blueprints

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    #this is t ensure that models is loaded before database is created
    from .models import User
    create_database(app)

    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    """if database doesnt already exist, create it"""
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
        print('Created Database!')