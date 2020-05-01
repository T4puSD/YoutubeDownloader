import os
import time
# import json
import pyperclip
from configparser import ConfigParser
from config import generateConfigFile
from advancedyvdown import logging
from notifier import notifyAboutTheService
from concurrent.futures import ThreadPoolExecutor, as_completed
from advancedyvdown import start_audio_download, start_video_download, start_high_quality_video_download


# genererating configure.ini file at first to
# load basic config files
if not os.path.exists(os.path.join('.','configure.ini')):
    generateConfigFile()
if os.path.exists(os.path.join('.','configure.ini')):
    config = ConfigParser()
    config.read('configure.ini')


MEDIA_TYPE = config['media_conf'].get('media_type')
MEDIA_QUALITY = config['media_conf'].get('media_quality')
DOWNLOAD_MODE = config['conf'].get('download_mode')

#defining threadpoolexecutor
executor = ThreadPoolExecutor(max_workers=3)

print(MEDIA_TYPE,MEDIA_QUALITY,DOWNLOAD_MODE)

notifyAboutTheService("Daemon Started","YoutubeDownloader is Running is the Background")


def handling_NewCopiedTask():
    futures = []
    # handling the daemon
    # discarding duplicate entry from the clipboard
    # and only taking new content from clipboard
    current_content = None
    while(True):
        content = pyperclip.paste()
        if content != current_content:
            current_content = content
            if content.startswith('https://www.youtube.com/watch?v=') and len(content.split("=")) > 1:
                # print(content)
                try:
                    if(MEDIA_TYPE == 'audio'):
                        futures.append(executor.submit(start_audio_download,content))
                    elif(MEDIA_TYPE == 'video'):
                        if(MEDIA_QUALITY == 'normal'):
                            futures.append(executor.submit(start_video_download,content))
                        elif(MEDIA_QUALITY == 'hq'):
                            futures.append(executor.submit(start_high_quality_video_download,content))
                    
                    for future in as_completed(futures):
                        try:
                            futures.remove(future)
                            if(len(futures) == 0):
                                logging.debug("No pending task in the list")
                        except Exception as e:
                            logging.debug("Error occured in removing future object from futures list")
                except Exception as e:
                    logging.debug("Error occured in daemon loop")

with ThreadPoolExecutor(max_workers=1) as threadExecutor:
    threadExecutor.submit(handling_NewCopiedTask)