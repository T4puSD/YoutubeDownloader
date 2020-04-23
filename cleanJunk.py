import os
import shutil
from advancedyvdown import logging
from config import conf

def cleanJunk():
    temp_dir = os.path.join(*conf.get('temp_dir'))
    try:
        shutil.rmtree(temp_dir)
    except Exception as e:
        logging.debug("Error occured cleaning temp_dir {}".format(temp_dir))

if __name__ == '__main__':
    cleanJunk()