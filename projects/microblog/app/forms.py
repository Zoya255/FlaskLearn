from flask_wtf import FlaskForm
from flask_babel import _
from flask_babel import lazy_gettext as _l
from wtforms import StringField, TextAreaField, PasswordField, BooleanField, SubmitField, RadioField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User
import re


class LoginForm(FlaskForm):
	login       = StringField( _l("Username"), validators = [ DataRequired(), Length( min=3, max=32 ) ] )
	password    = PasswordField( _l("Password"), validators = [ DataRequired(), Length( min=8, max=64 ) ] )
	remember_me = BooleanField( _l("Remember Me") )
	submit      = SubmitField( _l("Sign In") )


class RegistrationForm(FlaskForm):
	login     = StringField( _l("Username"), validators = [ DataRequired(), Length( min=3, max=32 ) ] )
	name      = StringField( _l("Name"), validators = [ DataRequired(), Length( min=2, max=32 ) ] )
	lastname  = StringField( _l("Lastname"), validators = [ DataRequired(), Length( min=2, max=32 ) ] )
	email     = StringField( _l("Email"), validators = [ DataRequired(), Email(), Length( min=7, max=64 ) ] )
	password  = PasswordField( _l("Password"), validators = [ DataRequired(), Length( min=8, max=64 ) ] )
	password2 = PasswordField( _l("Repeat password"), validators = [ DataRequired(), EqualTo( 'password' ) ] )
	submit    = SubmitField( _l("Register") )

	def validate_login( self, login ):
		user = User.query.filter_by( login = login.data ).first()
		if user is not None:
			raise ValidationError( _l("Please use a different login") )

		if re.search( '\W', login.data ):
			raise ValidationError( _l("Use only A-Z, a-z, 0-9 and _") )

	def validate_email( self, email ):
		user = User.query.filter_by( email = email.data ).first()
		if user is not None:
			raise ValidationError( _l("Please use a different email") )

	def validate_password( self, password ):
		if re.search('[a-z]', password.data) is None:
			raise ValidationError( _l("Use letter in password") )

		if re.search('[0-9]', password.data) is None:
			raise ValidationError( _l("Use number in password") )

		if re.search('[A-Z]', password.data) is None:
			raise ValidationError( _l("Use capital in password") )

		if re.search('[^A-Za-z0-9]', password.data) is None:
			raise ValidationError( _l("Use special chars in password") )


class EditProfileForm(FlaskForm):
	login       = StringField( _l("Username"), validators = [ DataRequired(), Length( min=2, max=32 ) ] )
	name        = StringField( _l("Name"), validators = [ DataRequired(), Length( min=2, max=32 ) ] )
	lastname    = StringField( _l("Lastname"), validators = [ DataRequired(), Length( min=2, max=32 ) ] )
	description = TextAreaField( _l("Description"), validators = [ DataRequired(), Length( min=0, max=256 ) ] )
	sex         = RadioField( _l("Sex"), choices = [ ("M", _l("Male") ), ("F", _l("Female") ), ("N", _l("None") ) ],
									  validators = [ DataRequired() ] )
	submit      = SubmitField( _l("Apply") )

	def __init__(self, orig_login, *args, **kwargs):
		super( EditProfileForm, self ).__init__(*args, **kwargs)
		self.orig_login = orig_login

	def validate_login( self, login ):
		if login.data != self.orig_login:
			user = User.query.filter_by( login = login.data ).first()
			if user is not None:
				raise ValidationError( _l("Please use a different login") )

			if re.search( '\W', login.data ):
				raise ValidationError( _l("Use only A-Z, a-z, 0-9 and _") )


class AddPostForm(FlaskForm):
	title   = StringField( _l("Title"), validators = [ DataRequired(), Length( min = 10, max = 50 ) ] )
	message = TextAreaField( _l("Message"), validators = [ DataRequired(), Length( min = 20, max = 256 ) ] )
	submit  = SubmitField( _l("Publish") )


class ResetPasswordRequestForm(FlaskForm):
	email  = StringField( _l("Email"), validators = [ DataRequired(), Email(), Length( min=7, max=64 ) ] )
	submit = SubmitField( _l("Reset Password") )

	def validate_email( self, email ):
		user = User.query.filter_by( email = email.data ).first()
		if user is None:
			raise ValidationError( _l("This email is not exist") )


class ResetPasswordForm(FlaskForm):
	password  = PasswordField( _l("Password"), validators = [ DataRequired(), Length( min = 8, max = 64 ) ] )
	password2 = PasswordField( _l("Repeat Password"), validators = [ DataRequired(), EqualTo( 'password' ) ] )
	submit    = SubmitField( _l("Reset Password") )

	def validate_password( self, password ):
		if re.search('[a-z]', password.data) is None:
			raise ValidationError( _l("Use letter in password") )

		if re.search('[0-9]', password.data) is None:
			raise ValidationError( _l("Use number in password") )

		if re.search('[A-Z]', password.data) is None:
			raise ValidationError( _l("Use capital in password") )

		if re.search('[^A-Za-z0-9]', password.data) is None:
			raise ValidationError( _l("Use special chars in password") )
