from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, BooleanField, SubmitField, RadioField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User
import re


class LoginForm(FlaskForm):
	login       = StringField( "Login", validators = [ DataRequired(), Length( min=3, max=32 ) ] )
	password    = PasswordField( "Password", validators = [ DataRequired(), Length( min=8, max=64 ) ] )
	remember_me = BooleanField( "Remember Me" )
	submit      = SubmitField( "Sign In" )


class RegistrationForm(FlaskForm):
	login     = StringField( "Login", validators = [ DataRequired(), Length( min=3, max=32 ) ] )
	name      = StringField( "Name", validators = [ DataRequired(), Length( min=2, max=32 ) ] )
	lastname  = StringField( "Lastname", validators = [ DataRequired(), Length( min=2, max=32 ) ] )
	email     = StringField( "Email", validators = [ DataRequired(), Email(), Length( min=7, max=64 ) ] )
	password  = PasswordField( "Password", validators = [ DataRequired(), Length( min=8, max=64 ) ] )
	password2 = PasswordField( "Repeat password", validators = [ DataRequired(), EqualTo( 'password' ) ] )
	submit    = SubmitField( "Register" )

	def validate_login( self, login ):
		user = User.query.filter_by( login = login.data ).first()
		if user is not None:
			raise ValidationError("Please use a different login")

		if re.search( '\W', login.data ):
			raise ValidationError( "Use only A-Z, a-z, 0-9 and _" )

	def validate_email( self, email ):
		user = User.query.filter_by( email = email.data ).first()
		if user is not None:
			raise ValidationError("Please use a different email")

	def validate_password( self, password ):
		if re.search('[a-z]', password.data) is None:
			raise ValidationError("Use letter in password")

		if re.search('[0-9]', password.data) is None:
			raise ValidationError("Use number in password")

		if re.search('[A-Z]', password.data) is None:
			raise ValidationError("Use capital in password")

		if re.search('[^A-Za-z0-9]', password.data) is None:
			raise ValidationError("Use special chars in password")


class EditProfileForm(FlaskForm):
	login       = StringField( "Login", validators = [ DataRequired(), Length( min=2, max=32 ) ] )
	name        = StringField( "Name", validators = [ DataRequired(), Length( min=2, max=32 ) ] )
	lastname    = StringField( "Lastname", validators = [ DataRequired(), Length( min=2, max=32 ) ] )
	description = TextAreaField( "Description", validators = [ DataRequired(), Length( min=0, max=256 ) ] )
	sex         = RadioField( "Sex", choices = [ ("M", "Male"), ("F", "Female"), ("N", "None") ],
									  validators = [ DataRequired() ] )
	submit      = SubmitField( "Apply" )

	def __init__(self, orig_login, *args, **kwargs):
		super( EditProfileForm, self ).__init__(*args, **kwargs)
		self.orig_login = orig_login

	def validate_login( self, login ):
		if login.data != self.orig_login:
			user = User.query.filter_by( login = login.data ).first()
			if user is not None:
				raise ValidationError("Please use a different login")

			if re.search( '\W', login.data ):
				raise ValidationError( "Use only A-Z, a-z, 0-9 and _" )


class AddPostForm(FlaskForm):
	title   = StringField( "Title", validators = [ DataRequired(), Length( min = 10, max = 50 ) ] )
	message = TextAreaField( "Message", validators = [ DataRequired(), Length( min = 20, max = 256 ) ] )
	submit  = SubmitField( "Publish" )


class ResetPasswordRequestForm(FlaskForm):
	email  = StringField( "Email", validators = [ DataRequired(), Email(), Length( min=7, max=64 ) ] )
	submit = SubmitField( "Reset Password" )

	def validate_email( self, email ):
		user = User.query.filter_by( email = email.data ).first()
		if user is None:
			raise ValidationError("This email is not exist")


class ResetPasswordForm(FlaskForm):
	password  = PasswordField( "Password", validators = [ DataRequired(), Length( min = 8, max = 64 ) ] )
	password2 = PasswordField( "Repeat Password", validators = [ DataRequired(), EqualTo( 'password' ) ] )
	submit    = SubmitField( "Reset Password" )

	def validate_password( self, password ):
		if re.search('[a-z]', password.data) is None:
			raise ValidationError("Use letter in password")

		if re.search('[0-9]', password.data) is None:
			raise ValidationError("Use number in password")

		if re.search('[A-Z]', password.data) is None:
			raise ValidationError("Use capital in password")

		if re.search('[^A-Za-z0-9]', password.data) is None:
			raise ValidationError("Use special chars in password")
