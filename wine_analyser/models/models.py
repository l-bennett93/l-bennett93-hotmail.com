from wine_analyser import db, login_manager, model
from flask_login import UserMixin

from joblib import load
from pathlib import Path
import sklearn
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    """
    This model contains all the users that have registered for the service
    """
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique = True, index = True)
    email = db.Column(db.String(64), unique = True, index = True)
    password = db.Column(db.String(120), nullable = False)
    sample_id = db.relationship("Sample", backref = "samples")

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"User {self.username}, email{self.email}"

class Sample(db.Model):
    __tablename__ = "samples"
    sample_id = db.Column(db.Integer, primary_key = True)
    customer_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    sample_id = db.Column(db.Integer, primary_key = True)
    customer_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    fixed_acidity = db.Column(db.String, nullable = False)
    volatile_acidity = db.Column(db.String, nullable = False)
    citric_acid = db.Column(db.String, nullable = False)
    residual_sugar = db.Column(db.String, nullable = False)
    chlorides = db.Column(db.String, nullable = False)
    free_sulfur_dioxide = db.Column(db.String, nullable = False)
    total_sulfur_dioxide = db.Column(db.String, nullable = False)
    density = db.Column(db.String, nullable = False)
    ph = db.Column(db.String, nullable = False)
    sulphates = db.Column(db.String, nullable = False)
    alcohol = db.Column(db.String, nullable = False)
    quality = db.Column(db.String)

    def __init__(self, customer_id, fixed_acidity, volatile_acidity,
                 citric_acid, residual_sugar, chlorides, free_sulfur_dioxide,
                 total_sulfur_dioxide, density, ph, sulphates, alcohol):

        self.customer_id = customer_id
        self.fixed_acidity = fixed_acidity
        self.volatile_acidity = volatile_acidity
        self.citric_acid = citric_acid
        self.residual_sugar = residual_sugar
        self.chlorides  = chlorides
        self.free_sulfur_dioxide = free_sulfur_dioxide
        self.total_sulfur_dioxide = total_sulfur_dioxide
        self.density = density
        self.ph = ph
        self.sulphates = sulphates
        self.alcohol = alcohol


        self.quality = self.predict_quality

    def __repr__(self):
        return f"Sample {self.sample_id}, User{self.customer_id}"

    @property
    def predict_quality(self):
        X = [
                self.fixed_acidity,
                self.volatile_acidity,
                self.citric_acid,
                self.residual_sugar,
                self.chlorides,
                self.free_sulfur_dioxide,
                self.density,
                self.total_sulfur_dioxide,
                self.ph,
                self.sulphates,
                self.alcohol
        ]
        X = [int(features) for features in X]

        X = model.predict([X])

        return str(X[0])
