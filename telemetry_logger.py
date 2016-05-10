#!/usr/bin/env python

from __future__ import print_function
import socket
import sys
import time
import pynmea2 as nmea

from sense_hat import SenseHat

import logging
import os.path
import datetime

def gps_dir(d):
	if(d == 'W' or d == 'S'):
		return -1
	return 1


class GPS:
	def __init__(self, addr="10:C6:FC:DA:67:AF"):

		connected = False
		while(not connected):
			try:
				self.sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
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


	def read(self):
		data = self.sock.recv(512)
		return data

	def close(self):
		self.sock.close()

	## Convert the GPS sentence into something we want to log
	#
	#  @param msg The msg as parsed by pynmea2
	#  @param sense A SenseHat class for grabbing readings.
	#
	# @returns a List on success or None on error.
	#
	def get_telemetry(self, msg, sense):
		if(isinstance(msg, nmea.GGA) or isinstance(msg, nmea.RMC)):
			speed = -1

			if(msg.lat is not None):
				lat = msg.latitude
			if(msg.lon is not None):
				lon = msg.longitude

			if(hasattr(msg, 'spd_over_grnd') and msg.spd_over_grnd is not None):
				speed = float(msg.spd_over_grnd)

			return [
				msg.timestamp.strftime('%H%M%S.%f'),
				lat, lon, speed
			] + sense.get_accel()

		return None

	def get_header(self):
		return [
			'timestamp', 'lat', 'lon,' 'speed', 'g_x', 'g_y', 'g_z'
		]


	


## Adds customs methods to SenseHat for reusability
#
class MySense(SenseHat):

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


	## Reformat the raw accelerometer readings  into
	#  something more list friendly.
	def get_accel(self):
		acr = self.get_accelerometer_raw()
		return [acr['x'], acr['y'], acr['z']]

## Get a timestamped logfile name
#
def get_log_filename(outputDir):
	filename = datetime.datetime.now().strftime('log_%Y_%m_%d_%H_%M.csv')
	return os.path.join(outputDir, filename)

## Function that handles all the actually logging.
#  This also performs log-file rotation
#
def do_logging(sense, outputDir):
	sense.show_waiting()
	gps = GPS()
	reader = nmea.NMEAStreamReader()

	sense.clear([0,255,0])

	logfile = None

	try:
		while(True):
			try:
				sense.show_logging()
				if(not logfile):
					logfile = open(get_log_filename(outputDir), 'w')
					logfile.write(','.join(gps.get_header())+'\n')
				for msg in reader.next(gps.read()):
					data = gps.get_telemetry(msg, sense)
					if(data is not None):
						logfile.write(','.join([str(x) for x in data])+'\n')


			except socket.error as e:
				# TODO: Log this error!
				sense.show_waiting()
				logging.error('Socket Error! '+str(e))
				gps = GPS()
				logfile.close()
				logfile = None

	except KeyboardInterrupt:
		sense.show_finished()
		gps.close()

if(__name__ == "__main__"):
	sense = MySense()
	sense.show_init();
	output_dir = '/var/log/telemetry'

	logging.basicConfig(filename=os.path.join(output_dir, 'error.log'), level=logging.INFO,
				format="%(asctime)s %(message)s")

	do_logging(sense, output_dir)
