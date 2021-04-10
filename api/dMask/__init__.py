from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
app.config["SECRET_KEY"] = "77a647040d624119619b0a9c46859930"
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db'

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"

from dMask import routes