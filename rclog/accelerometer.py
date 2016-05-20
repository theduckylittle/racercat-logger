## Contains classes for reading accelerometers
#

from . import Sensor

## Generic Class for Accelerometers
#
#  Defaults to returning 0 in the x,y,z directions.
#
class Accelerometer(Sensor):
	## Get the current accelerometer readings.
	#
	# @return dict with 'ax','ay','az' representing the accelerometers values.
	def read(self):
		return {'ax' : 0, 'ay' : 0, 'az' : 0}
	
	## Tell the writer to put the sensors in the x,y,z order
	#
	def order(self):
		return ['ax','ay','az']

## Const as to whether a SenseHat is connected
#  or not.
HAS_SENSE_HAT=True
try:
	from sense_hat import SenseHat
except ImportError:
	HAS_SENSE_HAT=False

if(HAS_SENSE_HAT):
	## Support reading the accelerometers from the
	#  RaspberryPi Sense Hat.
	class SenseHatAccelerometer(SenseHat):
		## Read the accelerometers from the sensehat
		#
		#  @returns An ax,ay,az dict of accelerometer readings
		#
		def read(self):
			acr = self.get_accelerometer_raw()
			return {
				'ax' : acr['x'], 
				'ay' : acr['y'], 
				'az' : acr['z']
			}

		## Tell the writer to put the sensors in the x,y,z order
		#
		def order(self):
			return ['ax','ay','az']
