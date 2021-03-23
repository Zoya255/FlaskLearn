from flask import url_for
from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.tokens import Tokens


class Followers(db.Model):
	id           = db.Column( db.Integer, primary_key = True )
	id_follower  = db.Column( db.Integer, db.ForeignKey( "user.id" ) )
	id_followed  = db.Column( db.Integer, db.ForeignKey( "user.id" ) )
	datetime_add = db.Column( db.DateTime, default = datetime.utcnow() )


class User(UserMixin, db.Model):
	id            = db.Column( db.Integer, primary_key = True )
	login         = db.Column( db.String(32), index = True, unique = True, nullable = False )
	name          = db.Column( db.String(32), nullable = False )
	lastname      = db.Column( db.String(32) )
	email         = db.Column( db.String(64), index = True, unique = True, nullable = False )
	pass_hash     = db.Column( db.String(128), nullable = False )
	description   = db.Column( db.String(256) )
	sex           = db.Column( db.String(1), default = 'N' )
	avatar_image  = db.Column( db.Integer, default = 10 )
	datetime_last = db.Column( db.DateTime, index = True, default = datetime.utcnow() )
	datetime_reg  = db.Column( db.DateTime, index = True, default = datetime.utcnow() )
	datetime_upd  = db.Column( db.DateTime, default = datetime.utcnow(), onupdate = datetime.utcnow() )

	posts = db.relationship( 'Post', backref = "author", lazy = "dynamic" )

	followed = db.relationship( 'User', secondary = Followers.__table__, primaryjoin = ( Followers.id_follower == id ),
								secondaryjoin = ( Followers.id_followed == id ),
								backref = db.backref( 'followers', lazy = "dynamic" ), lazy = "dynamic" )

	def __repr__(self):
		return f'<user {self.login}>'

	def set_password( self, password ):
		self.pass_hash = generate_password_hash(password)

	def check_password( self, password ):
		return check_password_hash(self.pass_hash, password)

	def avatar( self, size ):
		if self.avatar_image == 0:
			return None
		elif self.avatar_image is None:
			return url_for( 'static', filename = f"avatars/{size}/default_15.png" )
		else:
			return url_for( 'static', filename = f"avatars/{size}/default_{self.avatar_image}.png" )

	def follow( self, user ):
		if not self.is_following(user):
			self.followed.append(user)

	def unfollow( self, user ):
		if self.is_following(user):
			self.followed.remove(user)

	def is_following( self, user ):
		return self.followed.filter( Followers.id_followed == user.id ).count() > 0

	def followed_posts( self ):
		followed = Post.query.join(
			Followers, ( Followers.id_followed == Post.id_user ) ).filter(
				Followers.id_follower == self.id )
		own = Post.query.filter_by( id_user = self.id )
		return followed.union(own).order_by( Post.datetime_add.desc() )

	def get_reset_password_token( self ):
		t = Tokens()
		return t.encode( { "task": "reset_password", "id": self.id  } )

	@staticmethod
	def verify_reset_password_token( token ):
		t = Tokens()
		data = t.decode( token )

		if data["task"] == "reset_password":
			return User.query.get( data["id"] )


@login.user_loader
def load_user( id ):
	return User.query.get( int( id ) )


class Post(db.Model):
	id           = db.Column( db.Integer, primary_key = True )
	id_user      = db.Column( db.Integer, db.ForeignKey('user.id'), nullable = False )
	title        = db.Column( db.String(50), unique = True, nullable = False )
	message      = db.Column( db.String(200), nullable = False )
	datetime_add = db.Column( db.DateTime, index = True, default = datetime.utcnow )

	def __repr__(self):
		return f'<Post {self.title}>'

	def get_author( self ):
		author = User.query.get( self.id_user )
		return author.login

	def get_author_avatar( self, size ):
		author = User.query.get( self.id_user )

		if author.avatar_image == 0:
			return None
		elif author.avatar_image is None:
			return url_for( 'static', filename = f"avatars/{size}/default_15.png" )
		else:
			return url_for( 'static', filename = f"avatars/{size}/default_{author.avatar_image}.png" )

	@staticmethod
	def get_posts( user = None ):
		if user:
			return Post.query.filter_by( id_user = user.id ).order_by( Post.datetime_add.desc() )
		else:
			return Post.query.order_by( Post.datetime_add.desc() )
