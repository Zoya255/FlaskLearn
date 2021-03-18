from flask import url_for
from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


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

	posts = db.relationship( 'Post', backref = 'author', lazy = 'dynamic' )

	def __repr__(self):
		return f'{self.login}'

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


@login.user_loader
def load_user(id):
	return User.query.get(int(id))


class Post(db.Model):
	id           = db.Column( db.Integer, primary_key = True )
	id_user      = db.Column( db.Integer, db.ForeignKey('user.id'), nullable = False )
	title        = db.Column( db.String(50), unique = True, nullable = False )
	message      = db.Column( db.String(200), nullable = False )
	datetime_add = db.Column( db.DateTime, index = True, default = datetime.utcnow )

	def __repr__(self):
		return f'<Post {self.title}>'
