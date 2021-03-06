from app import app

@app.route('/')
@app.route('/index')
def index():
	return "<h1>Привет, Мир! Это мой первый сайт на Flask</h1>"

@app.route('/info')
def info():
	return "<h1>Тут нет ничего интересного. Пока.</h1>"