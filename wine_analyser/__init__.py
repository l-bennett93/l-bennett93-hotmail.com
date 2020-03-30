from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os
from pathlib import Path
from joblib import load


#Instantiate the app
app = Flask(__name__)

######################################
####SET UP RANDOM FOREST MODEL########
######################################
#Change this later to be a relative path.
file = Path("wine_analyser/networks/random_forest.pkl")
model = load(file)

#Instantiate the login manager
login_manager = LoginManager()
login_manager.init_app(app)

###########################
####DATABASE SETUP#########
###########################
dirname = os.path.abspath(os.path.dirname(__file__))

app.config["SECRET_KEY"] = "mysecretkey"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{dirname}data.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

db = SQLAlchemy(app)
Migrate(app, db)
