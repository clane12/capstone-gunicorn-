""""""

""" 
1. In our blog, the first registered user will be the admin. The admin user will be able to create new blog posts, 
   edit posts and delete posts.
2. The first user's id is 1. We can use this in index.html and post.html to make sure that only the admin user 
   can see the "Create New Post" and "Edit Post" and Delete buttons.
3. eg syntax. use this method for other as well like edit post or add a new post or create post etc.
        {% if current_user.id == 1 %}
          <a href="{{url_for('delete_post', post_id=post.id) }}">✘</a>
        {% endif %}
"""

""" Admin only decorator function create - make it so only admin or 1st registers user can access the add post etc functionalities.
1. What Happens When You Visit /admin
2. The @admin_only decorator is applied to the admin_dashboard function.
3. When a user visits the /admin route:
4. The inner decorated_function runs.
5. It checks if the current_user.id equals 1.
6. If yes, it allows access.
7. If no, it sends a 403 Forbidden error.

8. Using @wraps(f):

@wraps(f)
This preserves the name and docstring of the original function after decoration.

Without it, the decorated function would lose its identity.
"""


"""
1. author_id (Foreign Key in BlogPost) the foreign key determines that blogpost is many and users is one.
Holds the User ID to link the post to its author.
Used to store the relationship in the database.
Example:
Post ID 1 has author_id = 3.
Means: User with ID 3 wrote Post 1.

2. posts (Relationship in User)
Used to easily access all posts written by a particular user.
Without this relationship, you would have to manually search through the BlogPost table to find posts by that user.
Example:
user.posts gives you all posts written by that user in one go.

3. author (Relationship in BlogPost)
Used to easily access the author’s details from a post.
Without this, you would have to manually query the User table to get the author's information.
Example:
post.author.name directly gives you the name of the author.


"""




from datetime import date
from flask import Flask, abort, render_template, redirect, url_for, flash, request

from flask_bootstrap import Bootstrap5

from flask_ckeditor import CKEditor
# from flask_gravatar import Gravatar
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
import sqlalchemy

from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

# Import your forms from the forms.py
from forms import CreatePostForm, Register_form, Login_form, Comment_form

import os
from dotenv import load_dotenv
load_dotenv()



def admin_only(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        # Check if the current user is not the admin (id != 1)
        if current_user.id != 1:
            return abort(403)  # Return a 403 Forbidden error
        # If the user is an admin, call the original function
        return f(*args, **kwargs)
    return wrapper




app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
ckeditor = CKEditor(app)
Bootstrap5(app)

# TODO: Configure Flask-Login


# CREATE DATABASE
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_SQL')
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CONFIGURE TABLES
class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)

    author_id: Mapped[int] = mapped_column(String, db.ForeignKey("user.id"))
    author = relationship("User", back_populates='posts')
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)

    comments = relationship("User_comments", back_populates="parent_post")


# TODO: Create a User table for all your registered users. 
class User(UserMixin, db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False)

    posts = relationship("BlogPost", back_populates='author')

    comment = relationship('User_comments', back_populates='comment_author')


class User_comments(db.Model):
    __tablename__ = "user_comments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(String, nullable=False)

    author_id: Mapped[int] = mapped_column(Integer, db.ForeignKey('user.id'))
    comment_author = relationship('User', back_populates='comment')

    parent_post = relationship("BlogPost", back_populates="comments")
    post_id: Mapped[str] = mapped_column(Integer, db.ForeignKey("blog_posts.id"))

with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


# TODO: Use Werkzeug to hash the user's password when creating a new user.
@app.route('/register', methods=['POST', 'GET'])
def register():
    register = Register_form()
    if request.method == 'POST':
        email = register.email.data
        password = register.password.data
        name = register.name.data
        hashed_pass = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        add_user = User(name=name, password=hashed_pass, email=email)
        db.session.add(add_user)
        try:
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            flash("sorry! but there's already an account, with this email")
            return redirect(url_for('register'))
        else:
            login_user(add_user)
            return redirect(url_for('get_all_posts'))

    return render_template("register.html", register=register)


# TODO: Retrieve a user from the database based on their email. 
@app.route('/login', methods=['POST', 'GET'])
def login():
    login_form = Login_form()
    if request.method == 'POST':
        email = login_form.email.data
        password = login_form.password.data
        user = db.session.execute(db.select(User).where(User.email == email)).scalar()
        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('get_all_posts'))
            else:
                flash("Sorry! Wrong password, please try again")
                return redirect(url_for('login'))
        else:
            flash("sorry the account doesn't exist, please create a new one")
            return redirect(url_for('login'))
    return render_template("login.html", login = login_form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/')
def get_all_posts():
    result = db.session.execute(db.select(BlogPost))
    posts = result.scalars().all()
    return render_template("index.html", all_posts=posts)


# TODO: Allow logged-in users to comment on posts
@app.route("/post/<int:post_id>", methods=['POST', 'GET'])
# @login_required
def show_post(post_id):
    requested_post = db.get_or_404(BlogPost, post_id)
    comment = Comment_form()
    comments = db.session.execute(db.select(User_comments).where(User_comments.post_id == post_id)).scalars().all()
    if request.method == 'POST':
        user_comment = comment.comment.data
        add_comment = User_comments(text=user_comment, author_id= current_user.id, post_id=requested_post.id)
        db.session.add(add_comment)
        db.session.commit()
        return redirect(url_for('show_post', post_id=requested_post.id))

    return render_template("post.html", post=requested_post, comment=comment, comments=comments)


# TODO: Use a decorator so only an admin user can create a new post
@app.route("/new-post", methods=["GET", "POST"])
@login_required
@admin_only
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user,
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form)


# TODO: Use a decorator so only an admin user can edit a post
@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@login_required
@admin_only
def edit_post(post_id):
    post = db.get_or_404(BlogPost, post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = current_user
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))
    return render_template("make-post.html", form=edit_form, is_edit=True)


# TODO: Use a decorator so only an admin user can delete a post
@app.route("/delete/<int:post_id>")
@login_required
@admin_only
def delete_post(post_id):
    post_to_delete = db.get_or_404(BlogPost, post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=5002)
