from threading import Thread
from flask import render_template
from flask_mail import Message
from app import app, mail


def send_async_email( app, msg ):
	with app.app_context():
		mail.send( msg )


def send_email( title, sender, recipients, text_message, html_message ):
	msg = Message( title, sender = sender, recipients = recipients )
	msg.body = text_message
	msg.html = html_message
	Thread( target = send_async_email, args = ( app, msg ) ).start()


def send_template_email( title, sender, recipients, template_name, **kwargs ):
	msg = Message( title, sender = sender, recipients = recipients )
	msg.body = render_template( f"emails/{template_name}.txt", **kwargs )
	msg.html = render_template( f"emails/{template_name}.html", **kwargs )
	Thread( target = send_async_email, args = ( app, msg ) ).start()


def send_password_reset_email( user ):
	token = user.get_reset_password_token()

	send_template_email(
		title = "MicroBlog | Reset Password",
		sender = "MicroBlog <pass@microblog.com>",
		recipients = [ user.email ],
		template_name = "reset_password",
		user = user,
		token = token
	)
