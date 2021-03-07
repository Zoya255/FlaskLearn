from flask import render_template
from app import app


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
	return "<h1>Тут нет ничего интересного. Пока.</h1>"
