from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash


auth = Blueprint("auth", __name__)


@auth.route("/", methods=["GET", "POST"])
@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in", category="success")
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Password is incorrect", category="error")
        else:
            flash("Email does not exist", category="error")

    return render_template("login.html")


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(email=email).first()
        if email_exists:
            flash("Email already in use", category="error")
        elif username_exists:
            flash("Username already in use", category="error")
        elif password1 != password2:
            flash("Password does not match", category="error")
        elif len(username) < 2:
            flash("Username too short", category="error")
        elif len(password1) < 6:
            flash("Password too short", category="error")
        elif len(email) < 5:
            flash("Email invalid", category="error")
        else:
            new_user = User(
                email=email,
                username=username,
                password=generate_password_hash(password1, method="sha256"),
            )
            db.session.add(new_user)
            db.session.commit()
            flash("User created", category="success")
            return redirect(url_for("auth.login"))

    return render_template("signup.html")


@login_required
@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
