from flask import Flask
from flask_sqlalchemy import sqlalchemy
from flask_login import LoginManager

db-sqlalchemy()

def create_app():
     app=Flask(__name__,template_folder='templates')
     app.config['SECRET_KEY']='projectkey'
     app.config['SQLALCHEMY_DATABASE_URI']='sqlite:////db.sqlite3'

     db.init_app(app)



     from .views import views
     from .auth import auth 

     app.register_blueprint(views, url_prefix='/')
     app.register_blueprint(auth, url_prefix='/')
    
     return app