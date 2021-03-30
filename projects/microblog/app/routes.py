from flask import render_template, request, send_from_directory, flash, redirect, url_for, g
from flask_login import current_user, login_user, logout_user, login_required
from flask_babel import _, get_locale
from flask_babel import lazy_gettext as _l
from app import app, db, moment
from app.forms import LoginForm, RegistrationForm, EditProfileForm, AddPostForm,\
	ResetPasswordRequestForm, ResetPasswordForm
from app.models import User, Post
from werkzeug.urls import url_parse
from datetime import datetime
from app.emails import send_email, send_password_reset_email
from app.paginate import is_pages


# ------------------------ main pages ------------------------ #


@app.route('/')
@app.route('/index')
def index():
	page  = request.args.get( 'page', 1, type = int )
	posts = Post().get_posts().paginate( page, app.config['POSTS_PER_PAGE'], False )

	next_url, prev_url = is_pages( posts, "index" )

	return render_template( "index.html", title = _('Main page'), posts = posts.items, next_url = next_url, prev_url = prev_url )


@app.route('/feed')
@login_required
def feed():
	page = request.args.get( 'page', 1, type = int )
	posts = current_user.followed_posts().paginate( page, app.config['POSTS_PER_PAGE'], False )

	next_url, prev_url = is_pages( posts, "feed" )

	return render_template( "index.html", title = _('News feed'), posts = posts.items, next_url = next_url, prev_url = prev_url )


# ------------------------ login system ------------------------ #


@app.route('/login', methods = ['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect( url_for("index") )

	form = LoginForm()

	if form.validate_on_submit():
		user = User.query.filter_by( login = form.login.data ).first()

		if user is None or not user.check_password( form.password.data ):
			flash(_("Invalid login or password"))
			return redirect( url_for("login") )

		login_user( user, remember = form.remember_me.data )
		next_page = request.args.get( "next" )

		if not next_page or url_parse( next_page ).netloc != '':
			next_page = url_for( "index" )

		flash( _( "Congratulations, you are success login!" ) )
		app.logger.info( f'LOGIN    | success login user {user.login}' )

		return redirect( next_page )

	return render_template( "login.html", title = _('Login'), form = form )


@app.route('/register', methods = ['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect( url_for("index") )

	form = RegistrationForm()

	if form.validate_on_submit():
		user = User( login = form.login.data, email = form.email.data, name = form.name.data, lastname = form.lastname.data )
		user.set_password( password = form.password.data )

		db.session.add(user)
		db.session.commit()

		flash( _("Congratulations, you are now a registered user!") )
		app.logger.info( f'REGISTER | success registered user {user.login}' )

		return redirect( url_for("login") )

	return render_template( "register.html", title = _('Registration'), form = form )


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

	next_url, prev_url = is_pages( posts, "user", login = login )

	return render_template( "user_posts.html", title = f'{login}', user = user, posts = posts.items,
	                                           next_url = next_url, prev_url = prev_url )


@app.route('/user/<string:login>/followers')
def user_followers(login):
	page = request.args.get( 'page', 1, type = int )
	user = User.query.filter_by( login = login ).first_or_404()
	followers = user.followers.paginate( page, app.config['POSTS_PER_PAGE'], False )

	next_url, prev_url = is_pages( followers, "user_followers", login = login )

	return render_template( "user_followers.html", title = f'{login}', user = user, followers = followers.items,
	                                               next_url = next_url, prev_url = prev_url )


@app.route( '/user/<string:login>/followed' )
def user_followed(login):
	page = request.args.get( 'page', 1, type = int )
	user = User.query.filter_by( login = login ).first_or_404()
	followed = user.followed.paginate( page, app.config['POSTS_PER_PAGE'], False )

	next_url, prev_url = is_pages( followed, "user_followed", login = login )

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
		flash( _("Success update profile") )
		return redirect( url_for( 'edit_profile' ) )

	elif request.method == 'GET':
		form.login.data       = current_user.login
		form.name.data        = current_user.name
		form.lastname.data    = current_user.lastname
		form.description.data = current_user.description
		form.sex.data         = current_user.sex

	return render_template( "settings.html", title = _('Change of profile'), form = form )


@app.route('/add_post', methods = ['GET', 'POST'])
@login_required
def add_post():
	form = AddPostForm()

	if form.validate_on_submit():
		post = Post( id_user = current_user.id, title = form.title.data, message = form.message.data )
		db.session.add(post)
		db.session.commit()
		flash( _("Your post already on site") )
		return redirect( url_for( 'index' ) )

	return render_template( "add_post.html", title = _('New post'), form = form )


# ------------------------ api pages ------------------------ #


@app.route('/api/follow/<string:login>')
@login_required
def follow(login):
	user = User.query.filter_by( login = login ).first()

	if user is None:
		flash( _("User %(login)s not found", login = login) )
		return redirect( url_for( "index" ) )

	if user == current_user:
		flash( _("You connect follow yourself") )
		return redirect( url_for( "user", login = login ) )

	current_user.follow(user)
	db.session.commit()

	flash( _("You are following %(login)s", login = login) )
	return redirect( url_for( "user", login = login ) )


@app.route('/api/unfollow/<string:login>')
@login_required
def unfollow(login):
	user = User.query.filter_by( login = login ).first()

	if user is None:
		flash( _("User %(login)s not found", login = login ) )
		return redirect( url_for( "index" ) )

	if user == current_user:
		flash( _("You connect unfollow yourself") )
		return redirect( url_for( "user", login = login ) )

	current_user.unfollow(user)
	db.session.commit()

	flash( _("You are unfollow %(login)s", login = login ) )
	return redirect( url_for( "user", login = login ) )


@app.route( '/api/reset_password_request', methods = ['GET', 'POST'] )
def reset_password_request():
	if current_user.is_authenticated:
		return redirect( url_for( "index" ) )

	form = ResetPasswordRequestForm()

	if form.validate_on_submit():
		user = User.query.filter_by( email = form.email.data ).first()

		if user:
			send_password_reset_email(user)

		flash( _( "Check your email" ) )
		return redirect( url_for( "login" ) )

	return render_template( "reset_password_request.html", form = form )


@app.route( '/api/reset_password/<token>', methods = [ 'GET', 'POST' ] )
def reset_password(token):
	if current_user.is_authenticated:
		return redirect( url_for( "index" ) )

	user = User.verify_reset_password_token(token)

	if not user:
		flash( _("Invalid token") )
		return redirect( url_for( "index" ) )

	form = ResetPasswordForm()

	if form.validate_on_submit():
		user.set_password( form.password.data )
		db.session.commit()
		flash( _("Your password has been reset") )
		return redirect( url_for( "login" ) )

	return render_template( "reset_password.html", title = _('Reset Password'), form = form )


# ------------------------ technical pages ------------------------ #


@app.route('/favicon.ico')
@app.route('/robots.txt')
@app.route('/sitemap.xml')
def static_from_root():
	return send_from_directory(app.static_folder, request.path[1:])


@app.errorhandler(404)
def error_404(e):
	return render_template("404.html", title = _('Error 404') ), 404


@app.errorhandler(500)
def error_500(e):
	return render_template("500.html", title = _('Error 500') ), 500


@app.before_request
def before_request():
	if current_user.is_authenticated:
		current_user.datetime_last = datetime.utcnow()
		db.session.commit()

	g.locale = str( get_locale() )
