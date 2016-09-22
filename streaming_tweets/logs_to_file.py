import os
from os import path
import logging
from logging.handlers import RotatingFileHandler

def configuration_of_the_logs():
	"""logs configuration

	Warning: make sure there is a filename 'logs.txt' inside of
	a folder named 'logs'

	Returns:
		Object -- a logging object
	"""
	log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')

	#todo:#Check to see if the folder exist
	my_path = path.dirname(path.realpath(__file__))
	logFile = my_path + '/logs/logs.txt'

	#The logs.txt file can't be more than 5MB
	my_handler = RotatingFileHandler(logFile, mode='a', maxBytes=5*1024*1024,
	                                 backupCount=2, encoding=None, delay=0)
	my_handler.setFormatter(log_formatter)
	my_handler.setLevel(logging.INFO)

	app_log = logging.getLogger('root')
	#app_log.setLevel(logging.INFO)
	app_log.setLevel(logging.INFO)

	app_log.addHandler(my_handler)
	app_log.info('configuraring the logs')

	return app_log


if __name__ == '__main__':
    app_log = configuration_of_the_logs()
    app_log.info('this is a test for the log')
    while True:
    	  app_log.info("data")
        #app_log.warning("donnees")
        #app_log.warning('%s before you %s', 'Look', 'leap!')
