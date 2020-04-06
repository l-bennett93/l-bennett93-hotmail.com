from wine_analyser import app, db
from flask import Blueprint, render_template, redirect, url_for, request
from wine_analyser.users.forms import UserRegistrationForm, UserLoginForm
from wine_analyser.models import User
from flask_login import login_user, login_required, logout_user, current_user


users_blueprint = Blueprint('users', __name__,
                            template_folder = 'templates/users')

@users_blueprint.route("/login", methods = ["GET", "POST"])
def login():
    form = UserLoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            next = request.args.get("next")
            if next == None or not next[0] == "/":
                next = url_for("samples.dashboard")
            return redirect(next)
    return render_template("login.html", form = form)


@users_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@users_blueprint.route("/registration", methods = ["GET", "POST"])
def registration():
    form = UserRegistrationForm()
    if form.validate_on_submit():
        user = User(username = form.username.data,
                    email = form.email.data,
                    password = form.password.data)

        db.session.add(user)
        db.session.commit()
        return redirect(url_for("users.login"))
    return render_template("registration.html", form = form)
