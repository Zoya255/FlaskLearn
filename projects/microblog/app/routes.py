from flask import render_template, request
from app import app
from app.forms import LoginForm


@app.route('/')
@app.route('/index')
def index():
	info = {
		'title': 'Стартовая страница'
	}
	user = {
		'name': 'Халва'
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

	return render_template( "index.html", info = info, user = user, posts = posts )


@app.route('/info')
def info():
	info = {
		'title': 'Стартовая страница'
	}
	user = {
		'name': 'Халва'
	}

	data = f"Тут есть важная инфа: {app.config['SECRET_KEY']}"

	return render_template("info.html", info = info, user = user, data = data)


@app.route('/user/<int:user_id>/')
def user(user_id):
	info = {
		'title': 'Стартовая страница'
	}
	user = {
		'name': 'Халва'
	}

	data = f"Hello, {user_id}"

	return render_template("info.html", info = info, user = user, data = data)


@app.route('/test')
def requestdata():
	info = {
		'title': 'Стартовая страница'
	}
	user = {
		'name': 'Халва'
	}

	return render_template( "test.html", info = info, user = user, request = request )


@app.route('/login')
def login():
	info = {
		'title': 'Вход в систему'
	}
	user = {
		'name': 'Халва'
	}
	form = LoginForm()

	return render_template( "login.html", info = info, user = user, form = form )
