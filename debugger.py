import os
import logging
from configparser import ConfigParser
from config import generateConfigFile

# genererating configure.json file at first to
# load basic config files
if not os.path.exists(os.path.join('.','configure.ini')):
    generateConfigFile()
if os.path.exists(os.path.join('.','configure.ini')):
    config = ConfigParser()
    config.read('configure.ini')
# Setting up logger
# filename=LOG_FILE
logging.basicConfig(filename= os.path.join(*config['conf'].get('log_file').split(',')),
					level=logging.DEBUG,
					format = "%(asctime)s:%(levelname)s:%(filename)s:%(lineno)d:%(message)s"
					)
# logging to both file and to console with this streamhandler
# if console output is no longer needed commnet this line bellow
logging.getLogger().addHandler(logging.StreamHandler())