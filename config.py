import os
import pathlib
from configparser import ConfigParser

CONFIG_FILE_NAME = 'configure.ini'
config = ConfigParser()

home = pathlib.Path('.').absolute().home()
# hard coding the default download folder
user_download_folder = os.path.join(home,"Downloads")
default_download_folder = os.path.join(user_download_folder,"YoutubeMusic")
down_dir_audio = os.path.join(default_download_folder,"Audio")
down_dir_video = os.path.join(default_download_folder,"Video")

config['conf'] = {
    'download_dir': default_download_folder,
    'download_dir_audio':down_dir_audio,
    'download_dir_video':down_dir_video,
    'temp_dir':'temp',
    'log_file':'log.txt',
    'download_mode':'single',
    'number_of_threads':'2'
}

config['media_conf'] = {
    'media_type':'audio',
    'media_quality':'normal'
}

def initConfigFile():
    # genererating configure.ini file at first to
    # load basic config files
    config = None
    if not os.path.exists(os.path.join('.','configure.ini')):
        generateConfigFile()
    if os.path.exists(os.path.join('.','configure.ini')):
        config = ConfigParser()
        config.read('configure.ini')
    return config

def getConfigInstance():
    """Return config parser object to the caller
    Returns:
        ConfigParser object -- the config object created earlier will be returned 
    """    
    if not os.path.exists(os.path.join('.',CONFIG_FILE_NAME)):
        generateConfigFile()
        return config
    else: 
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
            config.write(configfile)

if __name__ == '__main__':
    generateConfigFile()
