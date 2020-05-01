import os
from configparser import ConfigParser

def generateConfigFile(confini = None):
    if confini !=None:
        with open('configure.ini','w') as configfile:
            confini.write(configfile)
    else:
        with open('configure.ini','w') as configfile:
            config.write(configfile)

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

if __name__ == '__main__':
    generateConfigFile()
