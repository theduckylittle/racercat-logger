## Log Writers

import csv

## Generic log writer
#  
#  To be be inherted by actual log writers.
#
class LogWriter:
	## Open the log for writing.
	#
	#  @param order The order for observation elements 
	#
	def open(self, order, **kwargs):
		self.order = order

	## Close the log after writing has finished
	#
	def close(self):
		pass

	## Write the log entry to a file.
	#
	#  @param observation A dict to be ordered by self.order 
	#                     and them written.
	# 
	def write(self, observation):
		raise Exception('"write" method should have been overridden by subclas')


	## Sync the loggers time represenation
	#  
	#  @param dt A python datetime object.
	#
	def sync_time(self, dt):
		self.datetime = dt

## Get a timestamped logfile name
#
def get_log_filename(outputDir):
	filename = datetime.datetime.now().strftime('log_%Y_%m_%d_%H_%M.csv')
	return os.path.join(outputDir, filename)


## Log to a file
#
class FileLogWriter(LogWriter):
	## Constructor
	# 
	#  Sets the filestream "out" to None, the internal flag
	#  indicating it has not been opened yet.
	#
	def __init__(self, **kwargs):
		self.out = None
		self.stream = None
		if('filename' not in kwargs):
			raise KeyError('Missing "filename" parameter for FileLogWriter')
		self.filename = kwargs['filename']


	## Open a file for writing
	#
	#  @param order The order for observation elements 
	#  @param kwargs Requires a parameter "filename"!
	#
	def open(self, order, **kwargs):
		LogWriter.open(self, order, **kwargs)

		# get the filename
		filename = self.datetime.strftime(self.filename)
		# open the file for writing
		self.stream = open(filename, 'w')
		# use the csv writer to ensure the output is safe.
		self.out = csv.writer(self.stream)
	
	## Close the file
	def close(self):
		self.stream.close()
		self.stream = None
		self.out = None

	## Write to the file. 
	def write(self, observation):
		# convert the dict to a list based on self.order,
		#  if the key is missing, "blank" it out with '',
		#  then write it to the csv file.
		self.out.writerow([observation.get(key, '') for key in self.order])

