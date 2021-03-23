import pytest
import os
from app import app, db
from app.models import User, Post
from app.generators import Generators
from app.tokens import Tokens


DROP  = True
PRINT = False
ITER  = 10
POSTS = 5


def setup_module():
	basedir = os.path.abspath( os.path.dirname( __file__ ) )
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join( basedir, 'test.db' )
	db.create_all()


def teardown_module():
	if DROP:
		db.session.remove()
		db.drop_all()
	else:
		pass


def test_password_hash():
	u = User( login = "test", name = "тест", lastname = "тест", email = "test@test.com" )
	g = Generators()

	for i in range( ITER ):
		password = g.random_string( 40, 10, True )
		u.set_password( password )

		assert u.check_password( password )


def test_tokens():
	g = Generators()
	t = Tokens()

	for i in range( ITER ):
		str1 = g.random_string( 4, 2 )
		str2 = g.random_string( 4, 2 )

		token = t.encode( { str1 : str2 } )
		data  = t.decode( token )

		if PRINT:
			print( token )
			print( data )

		assert data[str1] == str2


def test_users_create():
	g = Generators()

	for i in range( ITER ):
		login    = g.random_string( 10, 5 )
		name     = g.random_rus_string( 15, 10 )
		lastname = g.random_rus_string( 15, 10 )
		email    = g.random_string( 10, 5 )
		avatar   = g.random_string( 1, 16 )
		password = g.random_string( 40, 10, True )

		u = User( login = login, name = name, lastname = lastname, email = f"{email}@si.com", avatar_image = avatar )
		u.set_password( password )

		db.session.add(u)
		db.session.commit()


def test_user_select():
	for i in range( 1, ITER + 1 ):
		if PRINT:
			print( i, User.query.get( i ) )
		else:
			User.query.get( i )


def test_users_tokens():
	g = Generators()

	for i in range( 1, ITER + 1 ):
		user  = User.query.get( i )
		token = user.get_reset_password_token()

		assert User.verify_reset_password_token( token ) == user


def test_posts_create():
	g = Generators()

	for i in range( 1, ITER + 1 ):
		u = User.query.get( i )

		for j in range( POSTS ):
			title   = g.random_rus_string( 30, 15 )
			message = g.random_rus_string( 200, 30 )

			p = Post( id_user = i, title = title, message = message )

			db.session.add(p)

		db.session.commit()


def test_posts_select():
	for i in range( 1, ITER * POSTS + 1 ):
		if PRINT:
			print( i, Post.query.get( i ) )
		else:
			Post.query.get( i )


def test_follow_none():
	for i in range( 1, ITER + 1 ):
		u = User.query.get( i )

		assert u.followed.all() == []
		assert u.followers.all() == []


def test_follow_check():
	g = Generators()

	for i in range( 1, ITER ):
		u1 = User.query.get( i )
		u2 = User.query.get( i + 1 )

		u1.follow( u2 )
		db.session.commit()

		assert u1.is_following( u2 ) == True
		assert u1.followed.count() == 1
		assert u2.followers.count() == 1

		u1.unfollow( u2 )
		db.session.commit()

		assert u2.is_following( u2 ) == False
		assert u1.followed.count() == 0
		assert u2.followers.count() == 0


def test_follow_posts_select():
	for i in range( 1, ITER + 1 ):
		u = User.query.get( i )

		if PRINT:
			print( u.followed_posts().all() )
