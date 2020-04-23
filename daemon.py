import os
import time
import pyperclip
from advancedyvdown import logging
from config import conf,download_conf
from notifier import notifyAboutTheService
from concurrent.futures import ThreadPoolExecutor, as_completed
from advancedyvdown import start_audio_download, start_video_download, start_high_quality_video_download

MEDIA_TYPE = download_conf.get('media_type')
MEDIA_QUALITY = download_conf.get('media_quality')
DOWNLOAD_MODE = download_conf.get('download_mode')

#defining threadpoolexecutor
executor = ThreadPoolExecutor(max_workers=3)

print(MEDIA_TYPE,MEDIA_QUALITY,DOWNLOAD_MODE)

notifyAboutTheService("Daemon Started","YoutubeDownloader is Running is the Background")

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
                if(download_conf.get('media_type') == 'audio'):
                    futures.append(executor.submit(start_audio_download,content))
                elif(download_conf.get('media_type') == 'video'):
                    if(download_conf.get('media_quality') == 'normal'):
                        futures.append(executor.submit(start_video_download,content))
                    elif(download_conf.get('media_quality') == 'hq'):
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