from flask import render_template, request, send_from_directory, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User
from werkzeug.urls import url_parse


# ------------------------ main page ------------------------ #


@app.route('/')
@app.route('/index')
def index():
	info = {
		'title': 'Стартовая страница'
	}
	posts = [
		{
			'author': 'John',
			'title': 'Avengers'
		},
		{
			'author': 'John',
			'title': 'Avengers: Age of Altron'
		},
		{
			'author': 'John',
			'title': 'Avengers: Infinity War'
		},
		{
			'author': 'John',
			'title': 'Avengers: Endgame'
		},
		{
			'author': 'Scout',
			'title': 'Notes about Portland'
		},
	]

	return render_template( "index.html", info = info, posts = posts )


# ------------------------ login system ------------------------ #


@app.route('/login', methods = ['GET', 'POST'])
def login():
	info = {
		'title': 'Вход в систему'
	}

	if current_user.is_authenticated:
		return redirect( url_for("index") )

	form = LoginForm()

	if form.validate_on_submit():
		user = User.query.filter_by( login = form.login.data ).first()

		if user is None or not user.check_password( form.password.data ):
			flash("Invalid login or password")
			return redirect( url_for("login") )

		login_user( user, remember = form.remember_me.data )
		next_page = request.args.get( "next" )

		if not next_page or url_parse( next_page ).netloc != '':
			next_page = url_for( "index" )

		return redirect( next_page )

	return render_template( "login.html", info = info, form = form )


@app.route('/register', methods = ['GET', 'POST'])
def register():
	info = {
		'title': 'Регистрация'
	}

	if current_user.is_authenticated:
		return redirect( url_for("index") )

	form = RegistrationForm()

	if form.validate_on_submit():
		user = User( login = form.login.data, email = form.email.data,
		             name = form.name.data, lastname = form.lastname.data )
		user.set_password( password = form.password.data )

		db.session.add(user)
		db.session.commit()

		flash( "Congratulations, you are now a registered user!" )
		return redirect( url_for("login") )

	return render_template( "register.html", info = info, form = form )


@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for( "index" ))


# ------------------------ test pages ------------------------ #


@app.route('/user')
def user():
	info = {
		'title': 'Стартовая страница'
	}

	data = f"Hello, {current_user.login}"

	return render_template("info.html", info = info, data = data)


@app.route('/test')
def request_data():
	info = {
		'title': 'Стартовая страница'
	}

	return render_template( "test.html", info = info, request = request )


@app.route('/info')
def info():
	info = {
		'title': 'Стартовая страница'
	}

	data = f"Тут есть важная инфа: {app.config['SECRET_KEY']}"

	return render_template("info.html", info = info, data = data)


# ------------------------ technical pages ------------------------ #


@app.route('/favicon.ico')
@app.route('/robots.txt')
@app.route('/sitemap.xml')
def static_from_root():
	return send_from_directory(app.static_folder, request.path[1:])
