from time import time
import jwt
from app import app


class Tokens:
	def __init__( self, expiration_time = 600, key = app.config["SECRET_KEY"], algorithm = 'HS256' ):
		self.expiration_time = expiration_time
		self.key = key
		self.algorithm = algorithm

	def encode( self, data ):
		if self.expiration_time > 0:
			data["exp"] = time() + self.expiration_time
			data["iat"] = time()

		return jwt.encode( data, self.key, algorithm = self.algorithm )

	def decode( self, token ):
		try:
			return jwt.decode( token, self.key, algorithms = self.algorithm )
		except:
			return None
