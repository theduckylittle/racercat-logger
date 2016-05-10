from __future__ import print_function

import socket
import sys
import time
import logging

import pynmea2 as nmea

## Reads a Bluetooth GPS
#
class BluetoothGps:

	## Constructor
	#
	#  @param addr The bluetooth addresss of the GPS
	#
	def __init__(self, addr):

		connected = False
		while(not connected):
			try:
				self.sock = socket.socket(socket.AF_BLUETOOTH, 
				                socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
				self.sock.connect((addr, 1))
				connected = True
			except KeyboardInterrupt:
				sys.exit(0)
			except Exception as e:
				# TODO: Move to the logging library
				logging.error("Exception: "+str(e))
				logging.info("Could not connect. Waiting 10s")
				time.sleep(10)


		# set the timeout to 5 seconds.
		self.sock.settimeout(5)

	## Read data from the GPS feed
	#
	#  @returns Data read from the GPS
	def read(self):
		data = self.sock.recv(512)
		return data

	## Close the GPS 
	def close(self):
		self.sock.close()

	## Convert the GPS sentence into something we want to log
	#
	#  @param msg The msg as parsed by pynmea2
	#
	# @returns a List on success or None on error.
	#
	def get_position(self, msg):
		if(isinstance(msg, nmea.RMC)):
			speed = -1

			if(msg.lat is not None):
				lat = msg.latitude
			if(msg.lon is not None):
				lon = msg.longitude

			if(hasattr(msg, 'spd_over_grnd') and msg.spd_over_grnd is not None):
				speed = float(msg.spd_over_grnd)

			return {
				'timestamp' : msg.timestamp.strftime('%H%M%S.%f'),
				'lat' : lat, 'lon' : lon, 'knots' : speed
			} 
		return {}

	## Tell the writer the order of the gps fields
	#
	def order(self):
		return ['timestamp', 'lat', 'lon', 'knots']

