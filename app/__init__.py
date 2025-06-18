from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .database import db
from flask_login import LoginManager

import os

DB_NAME = "database.db"
basedir = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(basedir, "database.db")



def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'abcde'

    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_PATH}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from .routes import routes
    app.register_blueprint(routes)

    from .auth import auth
    app.register_blueprint(auth)

    from .models import User, Password

    with app.app_context():
        if not os.path.exists(DB_PATH):
            db.create_all()
            print("Created Database!")

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id): 
        return User.query.get(int(id))

    return app
