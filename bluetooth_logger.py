#!/usr/bin/env python

## This is an example of how to use racercat-logger
#  to construct a bluetooth GPS logger.
#  
#  This version will try to use the Raspberry Pi SenseHat
#  for display and accelerometers if available.
#

## Helpful commandline parsing tool
import click

## Assemble the useful components to start logging
from rclog import Logger, has_sensehat
from rclog.gps import BluetoothGps
from rclog.writer import FileLogWriter

import rclog.display
import rclog.accelerometer

import logging
import os.path


## Main function.
#
#  Configures the logger and gets things started.
@click.command()
@click.option('--addr', prompt='BT Address', help='Bluetooth GPS Address')
@click.option('--logdir', default='/var/log/racercat', help='Log output directory')
@click.option('--errorlog', default='/var/log/racercat/error.log', help='Filename for error log') 
def main(addr, logdir, errorlog):
	# configure the system logging
	logging.basicConfig(filename=errorlog, level=logging.INFO,
				format="%(asctime)s %(message)s")

	# start a generic display
	display = rclog.display.GenericDisplay()
	# no sensors
	sensors = []

	# if the sensehat is on and working, then
	#  use it for display and accelerometers.
	if(has_sensehat()):
		display = rclog.display.SenseHatDisplay()
		sensors.append(rclog.accelerometer.SenseHatAccelerometer())

	# setup a file writer,
	#  date and time variables are substituted using strftime when sync_time is called.
	writer = FileLogWriter(filename=os.path.join(logdir, 'log_%Y_%m_%d_%H_%M.csv'))
	
	# create a new logger instance
	logger = Logger(BluetoothGps, {'addr' : addr}, display, writer, sensors)
	logger.start()

## Oh python you quirky soul, start the main loop...
if(__name__ == "__main__"):
	main()
