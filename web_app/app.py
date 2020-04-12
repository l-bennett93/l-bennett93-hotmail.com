from wine_analyser import app, db
from flask import render_template, redirect, url_for, flash, request, jsonify
from wine_analyser.forms.forms import UserRegistrationForm, UserLoginForm, SampleForm
from wine_analyser.models.models import User, Sample
from flask_login import login_user, login_required, logout_user, current_user


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/login", methods = ["GET", "POST"])
def login():
    form = UserLoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            next = request.args.get("next")
            if next == None or not next[0] == "/":
                next = url_for("dashboard")
            return redirect(next)
    return render_template("login.html", form = form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/registration", methods = ["GET", "POST"])
def registration():
    form = UserRegistrationForm()
    if form.validate_on_submit():
        user = User(username = form.username.data,
                    email = form.email.data,
                    password = form.password.data)

        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("registration.html", form = form)

@app.route("/dashboard", methods = ["GET", "POST"])
@login_required
def dashboard():
    form = SampleForm()
    if form.validate_on_submit():
        sample = Sample(
            customer_id = current_user.id,
            fixed_acidity = form.fixed_acidity.data,
            volatile_acidity = form.volatile_acidity.data,
            citric_acid = form.citric_acid.data,
            residual_sugar = form.residual_sugar.data,
            chlorides = form.chlorides.data,
            free_sulfur_dioxide = form.free_sulfur_dioxide.data,
            total_sulfur_dioxide = form.total_sulfur_dioxide.data,
            density = form.density.data,
            ph = form.ph.data,
            sulphates = form.sulphates.data,
            alcohol = form.alcohol.data
        )
        db.session.add(sample)
        db.session.commit()
        return redirect(url_for("sample_analysis", sample_id = sample.sample_id))
    samples = Sample.query.filter_by(customer_id = current_user.id).all()
    return render_template("dashboard.html", form = form, samples = samples)

@app.route("/sample_analysis/<sample_id>")
@login_required
def sample_analysis(sample_id):
    sample = Sample.query.get(sample_id)
    return render_template("sample_analysis.html", sample=sample)

if __name__ == "__main__":
    app.run(debug=True)

