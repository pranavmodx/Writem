from flask_app import app, db
import requests
from flask import render_template, flash, redirect, url_for, abort, request
from flask_app.forms import RegistrationForm, LoginForm, TodoForm, BlogForm, DateForm
from flask_app.models import User, Todo, Blog
from flask_login import login_user, logout_user, current_user, login_required
from flask_app import bcrypt
import flask_app.handlers


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('You have registered successfully.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form, title='Register')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('You have logged in successfully.', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check email and password', 'danger')

    return render_template('login.html', form=form, title='Login')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/account')
@login_required
def account():
    return render_template('account.html', title='Account')


@app.route('/todo', methods=['GET', 'POST'])
@login_required
def todo():
    form = TodoForm()

    if form.validate_on_submit():
        task = Todo(title=form.title.data,
                    desc=form.desc.data, status=False, user=current_user)
        db.session.add(task)
        db.session.commit()

    return render_template('todos.html', form=form, title='Todos', complete=Todo.query.filter_by(status=True), incomplete=Todo.query.filter_by(status=False))


@app.route('/todo/<id>/complete')
def complete(id):
    # task = Todo.query.filter_by(id=id).first()
    task = Todo.query.get_or_404(id)

    # if task.user != current_user:
    #     abort(403)

    task.status = True
    db.session.commit()

    return redirect(url_for('todo'))


@app.route('/todo/<id>/incomplete')
def incomplete(id):
    # task = Todo.query.filter_by(id=id).first()
    task = Todo.query.get_or_404(id)

    # if task.user != current_user:
    #     abort(403)

    task.status = False
    db.session.commit()

    return redirect(url_for('todo'))


@app.route('/todo/<id>/delete')
def todo_delete(id):
    # task = Todo.query.filter_by(id=id).first()
    task = Todo.query.get_or_404(id)

    # if task.user != current_user:
    #     abort(403)

    db.session.delete(task)
    db.session.commit()

    return redirect(url_for('todo'))


@app.route('/todo/<id>/update', methods=['GET', 'POST'])
@login_required
def todo_update(id):
    # task = Todo.query.filter_by(id=id).first()
    task = Todo.query.get_or_404(id)

    if task.user != current_user:
        abort(403)

    form = TodoForm()

    if form.validate_on_submit():

        task.title = form.title.data
        task.desc = form.desc.data
        db.session.commit()
        flash('Your task has been updated!', 'success')

        return redirect(url_for('todo'))

    form.title.data = task.title
    form.desc.data = task.desc

    return render_template('todos_update.html', title='Update Task', form=form)


@app.route('/blog', methods=['GET', 'POST'])
@login_required
def blog():
    posts = Blog.query.all()
    form = BlogForm()

    if form.validate_on_submit():
        post = Blog(title=form.title.data,
                    content=form.content.data, user=current_user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('blog'))
    return render_template('blog.html', form=form, title='Blog Posts', posts=posts)


@app.route('/blog/<id>/delete')
def blog_delete(id):
    # post = Blog.query.filter_by(id=id).first()
    post = Todo.query.get_or_404(id)

    # if post.user != current_user:
    #     abort(403)

    db.session.delete(post)
    db.session.commit()

    return redirect(url_for('blog'))


@app.route('/blog/<id>/update', methods=['GET', 'POST'])
@login_required
def blog_update(id):
    post = Blog.query.get_or_404(id)

    if post.user != current_user:
        abort(403)

    form = BlogForm()

    if form.validate_on_submit():

        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')

        return redirect(url_for('blog'))

    form.title.data = post.title
    form.content.data = post.content

    return render_template('blogs_update.html', title='Update Post', form=form)


@app.route('/facts', methods=['GET', 'POST'])
def facts_finder():
    if request.method == 'POST':
        if request.form['num'] == 'Random':
            url = "http://numbersapi.com/random/date"
            r = requests.get(url)
            fact = r.text
            flash(fact)
            return redirect(url_for('facts_finder'))
        if request.form['num2'] == 'Choose Date':
            url = "http://numbersapi.com/random/date"
            r = requests.get(url)
            fact = r.text
            flash(fact)
            return redirect(url_for('facts_finder'))
    return render_template('facts.html', title='Facts Finder')
