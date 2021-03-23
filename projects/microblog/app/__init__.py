from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment

from datetime import datetime
from logging import Formatter, FileHandler, INFO, ERROR
from logging.handlers import SMTPHandler
import os

# ====== CONFIGS ======

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
mail = Mail(app)
moment = Moment(app)

app.jinja_env.auto_reload = True

# ====== MAIL ======

mail_handler = SMTPHandler(
	mailhost    = ( app.config['MAIL_SERVER'], app.config['MAIL_PORT'] ),
	fromaddr    = "MicroBlog <error@microblog.com>",
	toaddrs     = app.config['ADMIN_EMAILS'],
	subject     = "MicroBlog | Error",
	credentials = ( app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'] )
)
mail_handler.setLevel( ERROR )

app.logger.addHandler( mail_handler )
app.logger.setLevel( ERROR )

# ====== LOGS ======

if not os.path.exists('logs'):
	os.mkdir('logs')

now = datetime.now()
now = now.strftime("%Y-%m-%d")

file_formatter = Formatter( u'| %(filename)-15s | %(levelname)-8s | %(asctime)s | %(message)s', datefmt = '%H:%M:%S' )

file_handler = FileHandler( f"logs/log-{now}" )
file_handler.setFormatter( file_formatter )

app.logger.addHandler( file_handler )
app.logger.setLevel( INFO )

app.logger.info( 'SYSTEM   | Microblog startup' )

from app import routes, models
