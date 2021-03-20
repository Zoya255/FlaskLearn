from flask import render_template, request, send_from_directory, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, AddPostForm
from app.models import User, Post
from werkzeug.urls import url_parse
from datetime import datetime


# ------------------------ main pages ------------------------ #


@app.route('/')
@app.route('/index')
def index():
	page  = request.args.get( 'page', 1, type = int )
	posts = Post().get_posts().paginate( page, app.config['POSTS_PER_PAGE'], False )

	if posts.has_next:
		next_url = url_for( "index", page = posts.next_num )
	else:
		next_url = None

	if posts.has_prev:
		prev_url = url_for( "index", page = posts.prev_num )
	else:
		prev_url = None

	return render_template( "index.html", title = 'Главная', posts = posts.items,
	                                      next_url = next_url, prev_url = prev_url )


@app.route('/feed')
@login_required
def feed():
	page = request.args.get( 'page', 1, type = int )
	posts = current_user.followed_posts().paginate( page, app.config['POSTS_PER_PAGE'], False )

	if posts.has_next:
		next_url = url_for( "index", page = posts.next_num )
	else:
		next_url = None

	if posts.has_prev:
		prev_url = url_for( "index", page = posts.prev_num )
	else:
		prev_url = None

	return render_template( "index.html", title = 'Лента', posts = posts.items,
	                                      next_url = next_url, prev_url = prev_url )


# ------------------------ login system ------------------------ #


@app.route('/login', methods = ['GET', 'POST'])
def login():
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

		app.logger.info( f'LOGIN    | success login user {user.login}' )

		return redirect( next_page )

	return render_template( "login.html", title = 'Вход в систему', form = form )


@app.route('/register', methods = ['GET', 'POST'])
def register():
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
		app.logger.info( f'REGISTER | success registered user {user.login}' )
		return redirect( url_for("login") )

	return render_template( "register.html", title = 'Регистрация', form = form )


@app.route('/logout')
def logout():
	app.logger.info( f'LOGOUT   | success logout user {current_user.login}' )
	logout_user()
	return redirect( url_for( "index" ) )


# ------------------------ functional pages ------------------------ #


@app.route('/user/<string:login>')
def user(login):
	page = request.args.get( 'page', 1, type = int )
	user = User.query.filter_by( login = login ).first_or_404()
	posts = Post().get_posts(user).paginate( page, app.config['POSTS_PER_PAGE'], False )

	if posts.has_next:
		next_url = url_for( "index", page = posts.next_num )
	else:
		next_url = None

	if posts.has_prev:
		prev_url = url_for( "index", page = posts.prev_num )
	else:
		prev_url = None

	return render_template( "user_posts.html", title = f'{login}', user = user, posts = posts.items,
	                                           next_url = next_url, prev_url = prev_url )


@app.route('/user/<string:login>/followers')
def user_followers(login):
	page = request.args.get( 'page', 1, type = int )
	user = User.query.filter_by( login = login ).first_or_404()
	followers = user.followers.paginate( page, app.config['POSTS_PER_PAGE'], False )

	if followers.has_next:
		next_url = url_for( "index", page = followers.next_num )
	else:
		next_url = None

	if followers.has_prev:
		prev_url = url_for( "index", page = followers.prev_num )
	else:
		prev_url = None

	return render_template( "user_followers.html", title = f'{login}', user = user, followers = followers.items,
	                                               next_url = next_url, prev_url = prev_url )


@app.route( '/user/<string:login>/followed' )
def user_followed(login):
	page = request.args.get( 'page', 1, type = int )
	user = User.query.filter_by( login = login ).first_or_404()
	followed = user.followed.paginate( page, app.config['POSTS_PER_PAGE'], False )

	if followed.has_next:
		next_url = url_for( "index", page = followed.next_num )
	else:
		next_url = None

	if followed.has_prev:
		prev_url = url_for( "index", page = followed.prev_num )
	else:
		prev_url = None

	return render_template( "user_followed.html", title = f'{login}', user = user, followed = followed.items,
	                                              next_url = next_url, prev_url = prev_url )


@app.route('/edit_profile', methods = ['GET', 'POST'])
@login_required
def edit_profile():
	form = EditProfileForm(current_user.login)

	if form.validate_on_submit():
		current_user.login       = form.login.data
		current_user.name        = form.name.data
		current_user.lastname    = form.lastname.data
		current_user.description = form.description.data
		current_user.sex         = form.sex.data

		db.session.commit()
		flash( "Success update profile" )
		return redirect( url_for( 'edit_profile' ) )

	elif request.method == 'GET':
		form.login.data       = current_user.login
		form.name.data        = current_user.name
		form.lastname.data    = current_user.lastname
		form.description.data = current_user.description
		form.sex.data         = current_user.sex

	return render_template( "settings.html", title = 'Изменение профиля', form = form )


@app.route('/add_post', methods = ['GET', 'POST'])
@login_required
def add_post():
	form = AddPostForm()

	if form.validate_on_submit():
		post = Post( id_user = current_user.id, title = form.title.data, message = form.message.data )
		db.session.add(post)
		db.session.commit()
		flash("Your post already on site")
		return redirect( url_for( 'index' ) )

	return render_template( "add_post.html", title = 'Новый пост', form = form )


# ------------------------ api pages ------------------------ #


@app.route('/api/follow/<string:login>')
def follow(login):
	user = User.query.filter_by( login = login ).first()

	if user is None:
		flash( f"User {login} not found" )
		return redirect( url_for( "index" ) )

	if user == current_user:
		flash( f"You connect follow yourself" )
		return redirect( url_for( "user", login = login ) )

	current_user.follow(user)
	db.session.commit()

	flash( f"You are following {login}" )
	return redirect( url_for( "user", login = login ) )


@app.route('/api/unfollow/<string:login>')
def unfollow(login):
	user = User.query.filter_by( login = login ).first()

	if user is None:
		flash( f"User {login} not found" )
		return redirect( url_for( "index" ) )

	if user == current_user:
		flash( f"You connect unfollow yourself" )
		return redirect( url_for( "user", login = login ) )

	current_user.unfollow(user)
	db.session.commit()

	flash( f"You are not unfollow {login}" )
	return redirect( url_for( "user", login = login ) )


# ------------------------ test pages ------------------------ #


@app.route('/test')
def request_data():
	return render_template( "test.html", title = 'Тест' )


@app.route('/info')
def info():
	data = f"Тут есть важная инфа: {app.config['SECRET_KEY']}"

	return render_template( "info.html", title = 'Информация', data = data )


# ------------------------ technical pages ------------------------ #


@app.route('/favicon.ico')
@app.route('/robots.txt')
@app.route('/sitemap.xml')
def static_from_root():
	return send_from_directory(app.static_folder, request.path[1:])


@app.errorhandler(404)
def error_404(e):
	return render_template("404.html", title = 'Ошибка 404'), 404


@app.errorhandler(500)
def error_500(e):
	return render_template("500.html", title = 'Ошибка 500'), 500


@app.before_request
def before_request():
	if current_user.is_authenticated:
		current_user.datetime_last = datetime.utcnow()
		db.session.commit()
