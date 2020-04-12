from wine_analyser import app, db
from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from wine_analyser.samples.forms import SampleForm
from wine_analyser.models import Sample
from flask_login import login_user, login_required, logout_user, current_user

sample_blueprint = Blueprint('samples', __name__,
                            template_folder = 'templates/samples')

@sample_blueprint.route("/dashboard", methods = ["GET", "POST"])
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
        return redirect(url_for("samples.sample_analysis", sample_id = sample.sample_id))
    samples = Sample.query.filter_by(customer_id = current_user.id).all()
    return render_template("dashboard.html", form = form, samples = samples)

@sample_blueprint.route("/sample_analysis/<sample_id>")
@login_required
def sample_analysis(sample_id):
    sample = Sample.query.get(sample_id)
    return render_template("sample_analysis.html", sample=sample)
