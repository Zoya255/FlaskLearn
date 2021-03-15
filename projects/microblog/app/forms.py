from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
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

