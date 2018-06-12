# This is Exception Base Class

class BaseException(Exception):
	def __init__(self, *args):
		self.args= args
