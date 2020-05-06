import os
from configparser import ConfigParser

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
    if not os.path.exists(os.path.join('.','configure.ini')):
        generateConfigFile()
    return config

def generateConfigFile(confini = None):
    if confini !=None:
        with open('configure.ini','w') as configfile:
            confini.write(configfile)
    else:
        with open('configure.ini','w') as configfile:
            config.write(configfile)

if __name__ == '__main__':
    generateConfigFile()
