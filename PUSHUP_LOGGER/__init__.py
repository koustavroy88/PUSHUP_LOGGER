from flask import Flask, Blueprint
# from flask_sqlalchemy import SQLAlchemy
from .model import db,User
# db = SQLAlchemy()
from flask_login import LoginManager

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY']='secret-key'
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.sqlite'

    db.init_app(app)
    app.app_context().push()
    with app.app_context():
        db.create_all()
        print("Database Created")

    login_manager=LoginManager()
    login_manager.login_view='auth_bp.login'
    login_manager.init_app(app)


    with app.app_context():
        from .main import main_bp   
        from .auth import auth_bp

        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))
        app.register_blueprint(main_bp)
        app.register_blueprint(auth_bp)
        return app