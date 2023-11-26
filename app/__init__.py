from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ваш_секретний_ключ'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' 

login_manager = LoginManager(app)
login_manager.login_view = 'login'

db = SQLAlchemy(app)

from app.models import User  

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from app import views 
