from flask import render_template, url_for, flash, redirect, request, Response
from dMask import app, db, bcrypt
from dMask.forms import LoginForm, UpdateForm, RecoverForm, ResetForm
from dMask.models import User, Status
from flask_login import login_user, login_required, current_user
import cv2
import json


# Тестово
camera = cv2.VideoCapture(0)


def save_update_data(form, reset=False):
    admin = User.query.filter_by(id=1).first()
    if not reset:
        admin.username = form.username.data
        admin.secret = form.secret.data
    admin.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')    
    db.session.commit()


def check_credentials(username, password):
    admin = User.query.filter_by(username=username).first()
    if admin and bcrypt.check_password_hash(admin.password, password):
        login_user(admin)
        return True
    elif not admin:
        return "Username not found!"
    elif not bcrypt.check_password_hash(admin.password, password):
        return "Wrong password! Check your password and try again."


def recovery_check(form):
    admin = User.query.filter_by(username=form.username.data).first()
    if admin and form.secret.data == admin.secret:
        return True
    elif not admin:
        return "Username not found!"
    elif not form.secret.data == admin.secret:
        return "Secret answer does not match!"


@app.route("/")
@app.route("/home")
@login_required
def home():
    with open("messages.json", "r") as f:
        data = json.load(f)

    status = Status.query.filter_by(id=1).first()
    return render_template("home.html", title="Home", status=status, messages=data["messages"])

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if isinstance(check_credentials(form.username.data, form.password.data), bool):
            page = request.args.get("next")
            return redirect(page) if page else redirect(url_for("home"))
        else:
            flash(check_credentials(form.username.data, form.password.data))
    return render_template("login.html", title="Login", form=form)


@app.route("/update", methods=["GET", "POST"])
@login_required
def update():
    if not User.query.filter_by(id=1).first().secret:
        form = UpdateForm()
        if form.validate_on_submit():
            save_update_data(form)
            return redirect(url_for("home"))
        return render_template("update.html", title="Update", form=form)
    else:
        flash("You have already updated your credentials!")
        if current_user.is_authenticated:
            return redirect(url_for("home"))
        else:
            return redirect(url_for("login"))
        

@app.route("/recovery", methods=["GET", "POST"])
def recovery():
    form = RecoverForm()
    if form.validate_on_submit():
        if isinstance(recovery_check(form), bool):
            return redirect(url_for("reset"))
        else:
            flash(recovery_check(form))
    return render_template("recovery.html", title="Recovery", form=form)


@app.route("/reset", methods=["GET", "POST"])
def reset():
    form = ResetForm()
    if form.validate_on_submit():
        save_update_data(form, reset=True)
        return redirect(url_for("login"))
    return render_template("reset.html", title="Reset", form=form)