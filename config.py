import os
import pathlib
from configparser import ConfigParser

CONFIG_FILE_NAME = 'configure.ini'
# config = ConfigParser()

HOME = pathlib.Path('.').absolute().home()
# hard coding the default download folder
USER_DOWNLOAD_FOLDER = os.path.join(HOME,"Downloads")
DEFAULT_DOWNLOAD_FOLDER = os.path.join(USER_DOWNLOAD_FOLDER,"YoutubeMusic")


def constructConfig(DEFAULT_DOWNLOAD_FOLDER):
    DOWNLOAD_DIR_AUDIO = os.path.join(DEFAULT_DOWNLOAD_FOLDER,"Audio")
    DOWNLOAD_DIR_VIDEO = os.path.join(DEFAULT_DOWNLOAD_FOLDER,"Video")
    
    config = ConfigParser()
    config['conf'] = {
    'download_dir': DEFAULT_DOWNLOAD_FOLDER,
    'download_dir_audio':DOWNLOAD_DIR_AUDIO,
    'download_dir_video':DOWNLOAD_DIR_VIDEO,
    'temp_dir':'temp',
    'log_file':'log.txt',
    'download_mode':'single',
    'number_of_threads':'2'
    }

    config['media_conf'] = {
        'media_type':'audio',
        'media_quality':'normal'
    }
    return config


def initConfigInstance():
    """Return config parser object to the caller
    Returns:
        ConfigParser object -- the config object created earlier will be returned 
    """    
    if not os.path.exists(os.path.join('.',CONFIG_FILE_NAME)):
        config = constructConfig(DEFAULT_DOWNLOAD_FOLDER)
        generateConfigFile(config)
        return config
    else: 
        config = ConfigParser()
        config.read(CONFIG_FILE_NAME)
        return config

def generateConfigFile(confini = None):
    """persisting configure file to disk
    Keyword Arguments:
        confini {config object} -- ConfigParser object to persist (default: {None})
    """    
    if confini !=None:
        with open(CONFIG_FILE_NAME,'w') as configfile:
            # wrting modified config object provided as argument
            confini.write(configfile)
    else:
        with open(CONFIG_FILE_NAME,'w') as configfile:
            # no argument provided write the default object to file
            config = constructConfig(DEFAULT_DOWNLOAD_FOLDER)
            config.write(configfile)

if __name__ == '__main__':
    generateConfigFile()
