# This file defines various exception types this BidBot may encounter 
from BaseException import BaseException
class VcodeCaptureError(BaseException):
	def __init__(self, msg = '', args = ''):
		self.args = args
		self.message = msg

class LoginError(BaseException):
	def __init__(self):
		pass