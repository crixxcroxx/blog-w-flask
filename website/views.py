from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Post, User
from . import db

views = Blueprint("views", __name__)


@login_required
@views.route("/home")
def home():
    posts = Post.query.all()
    return render_template("home.html", user=current_user, posts=posts)


@login_required
@views.route("/create-post", methods=["GET", "POST"])
def create_post():
    if request.method == "POST":
        postText = request.form.get("post")

        if not postText:
            flash("Post cannot be empty", category="error")
        else:
            post = Post(post=postText, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash("Post created!", category="success")
            return redirect(url_for("views.home"))

    return render_template("create_post.html", user=current_user)


@login_required
@views.route("/delete-post/<id>")
def delete_post(id):
    post = Post.query.filter_by(id=id).first()
    if not post:
        flash("Post does not exist", category="error")
    elif current_user.id != post.author:
        flash("You do not have permission to delete this post", category="error")
    else:
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted!", category="success")

    return redirect(url_for("views.home"))


@login_required
@views.route("/posts/<username>")
def posts(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        flash("User does not exist", category="error")
        return redirect(url_for("views.home"))
    else:
        posts = Post.query.filter_by(author=user.id).all()
        return render_template(
            "posts.html", user=current_user, posts=posts, username=username
        )
