import os
from configparser import ConfigParser

CONFIG_FILE_NAME = 'configure.ini'
config = ConfigParser()

config['conf'] = {
    'download_dir_audio':'testdownloads2',
    'download_dir_video':'testdownloads2,video',
    'temp_dir':'temp',
    'log_file':'log.txt',
    'download_mode':'single',
    'number_of_threads':'2'
}

config['media_conf'] = {
    'media_type':'audio',
    'media_quality':'normal'
}

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
