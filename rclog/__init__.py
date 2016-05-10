
import pynmea2 as nmea
import socket
from datetime import datetime

## Generic [Empty] Sensor
#
class Sensor:
	## Constructor.  
	#
	# Does nothing by default.  This has been left here
	#  explicitly as an opportunity for others to add hooks
	#  as sensors are needed.
	#
	def __init__(self):
		pass

	## Read the sensor(s).
	#
	#  This should return a dict that contains the name
	#   of the sensor in the key and the value in the value.
	#
	# @return An empty dict for now.
	#
	def read(self):
		return {}

	## Describes the order in which the sensor data should 
	#  be written to the file.
	#
	def order(self):
		return []
	


## Main class for logging telemetry data.
# 
class Logger:
	## Constructor.
	#
	#  @param gpsClass The GPS Class to be used for reading, NOT AN INSTANCE, THE CLASS!
	#  @param gpsConfig Configuration parameters for the GPS class
	#  @param display Instance of a display class.
	#  @param writer A LogWriter instance that can be used to put the data.
	#  @param senors List of sensors to be read once a position is ready to be logged.
	#
	def __init__(self, gpsClass, gpsConfig, display, writer, sensors=[]):
		self.gpsClass = gpsClass 
		self.gpsConfig = gpsConfig
		self.display = display
		self.sensors = sensors
		self.writer = writer

		self.display.show_init()

	## Start logging
	def start(self):
		# Tell the user the logger is waiting on a GPS signal.
		self.display.show_waiting()

		# initialize a nmea stream reader
		reader = nmea.NMEAStreamReader()

		# Create a new GPS reader
		gps = self.gpsClass(**self.gpsConfig)

		# create the composite "ordering" of observation elements
		order = gps.order() 
		for sensor in self.sensors:
			order += sensor.order()
		
		log_ready = False
		try:
			while(True):
				try:
					for msg in reader.next(gps.read()):
						if(not log_ready):
							print str(msg)
							# convert the nmea/zda into something more
							#  generically useful.
							dt = datetime.combine(
								msg.datestamp, msg.timestamp
							)
							self.writer.sync_time(dt)
							self.writer.open(order)

							log_ready = True
							self.display.show_logging()
						else:
							# start logging once the log file exists
							data = gps.get_position(msg)
							# if the data is good then continue
							if('lat' in data):
								# add sensor information
								for sensor in self.sensors:
									data.update(sensor.read())
								# write the data out.
								self.writer.write(data)

				except socket.error as e:
					# TODO: Log this error!
					self.display.show_waiting()
					logging.error('Socket Error! '+str(e))
					gps = GPS(**gpsConfig)

					self.writer.close()
					log_ready = False

		except KeyboardInterrupt:
			self.display.show_finished()
			gps.close()


## Utility function to sniff for the sense hat
#

HAS_SENSE_HAT=True
try:
	from sense_hat import SenseHat
except ImportError:
	HAS_SENSE_HAT=False

def has_sensehat():
	return HAS_SENSE_HAT
