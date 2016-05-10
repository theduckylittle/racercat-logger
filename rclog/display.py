# Use print as a FUNCTION!
from __future__ import print_function

## Generic Class for Displaying Particular Data
#  while the logger is running
#
#
class GenericDisplay:
	## Constructor
	def __init__(self):
		## Generic loading message
		self.loading_message = 'Loading...'

	## Show a loading/initialization message
	#
	def show_init(self):
		print(self.loading_message)

	## Indicate to the user that the GPS has not
	#  yet connected.
	#
	def show_waiting(self):
		print('Waiting for GPS signal')

	## Tell the user that logging is happening
	#
	def show_logging(self):
		print('Logging...')

	
	## Show a "finished" message.  Not sure this
	#  is ever called in the current code.
	#
	def show_finished(self):
		print('Logging has ended')

## Const as to whether a SenseHat is connected
#  or not.
HAS_SENSE_HAT=True
try:
	from sense_hat import SenseHat
except ImportError:
	HAS_SENSE_HAT=False

if(HAS_SENSE_HAT):
	## Adds the "get_accel" class to the SenseHat base class.
	#
	class SenseHatDisplay(SenseHat):

		## Show a message that things are getting going.
		def show_init(self):
			self.show_message('Loading...')

		## Show a color to indicate that logging has
		#  not yet started. (Waiting on bluetooth).
		#
		def show_waiting(self):
			self.clear([255,0,0])

		## Show a color to indicate logging is working.
		#
		def show_logging(self):
			self.clear([0,155,0])

		## Show the checkered Flag!
		#
		def show_finished(self):
			X = (255,255,255)
			O = (0,0,0)

			flag = [
			 O,O, X,X, O,O, X,X,
			 O,O, X,X, O,O, X,X,
			 X,X, O,O, X,X, O,O,
			 X,X, O,O, X,X, O,O,
			 O,O, X,X, O,O, X,X,
			 O,O, X,X, O,O, X,X,
			 X,X, O,O, X,X, O,O,
			 X,X, O,O, X,X, O,O,
			]

			self.set_pixels(flag)
