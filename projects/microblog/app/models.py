from datetime import datetime
from app import db


class User(db.Model):
	id           = db.Column( db.Integer, primary_key = True )
	login        = db.Column( db.String(32), index = True, unique = True, nullable = False )
	name         = db.Column( db.String(32), nullable = False )
	lastname     = db.Column( db.String(32) )
	email        = db.Column( db.String(64), index = True, unique = True, nullable = False )
	pass_hash    = db.Column( db.String(128), nullable = False )
	datetime_reg = db.Column( db.DateTime, index = True, default = datetime.utcnow )

	posts = db.relationship( 'Post', backref = 'author', lazy = 'dynamic' )

	def __repr__(self):
		return f'<User {self.login}>'


class Post(db.Model):
	id           = db.Column( db.Integer, primary_key = True )
	id_user      = db.Column( db.Integer, db.ForeignKey('user.id'), nullable = False )
	title        = db.Column( db.String(50), unique = True, nullable = False )
	message      = db.Column( db.String(200), nullable = False )
	datetime_add = db.Column( db.DateTime, index = True, default = datetime.utcnow )

	def __repr__(self):
		return f'<Post {self.title}>'
