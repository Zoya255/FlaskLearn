import os
from dotenv import load_dotenv

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
	# Hardcode values
	POSTS_PER_PAGE = 20
	TEMPLATES_AUTO_RELOAD = True
	LANGUAGES = [ 'en', 'ru', 'es' ]

	# Users vars
	ADMIN_EMAILS = [ "codeoon@mail.ru", "optimazecode@gmail.com" ]
	SECRET_KEY   = os.environ.get( 'SECRET_KEY' )

	# DB vars
	SQLALCHEMY_DATABASE_URI        = os.environ.get( 'MySQL_DB' )
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	# Mail vars
	MAIL_SERVER   = os.environ.get( 'MAIL_SERVER' )
	MAIL_PORT     = os.environ.get( 'MAIL_PORT' )
	MAIL_USERNAME = os.environ.get( 'MAIL_USERNAME' )
	MAIL_PASSWORD = os.environ.get( 'MAIL_PASSWORD' )
	MAIL_USE_TLS  = os.environ.get( 'MAIL_USE_TLS' )
