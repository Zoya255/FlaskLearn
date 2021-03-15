from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
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

	def set_password( self, password ):
		self.pass_hash = generate_password_hash(password)

	def check_password( self, password ):
		return check_password_hash(self.pass_hash, password)


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
