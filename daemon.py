import os
import pyperclip
from threading import Thread
from queue import Queue
from configparser import ConfigParser
from concurrent.futures import as_completed
from config import generateConfigFile
from debugger import logging
from advancedyvdown import start_audio_download
from advancedyvdown import start_video_download
from advancedyvdown import start_high_quality_video_download

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
NUMBER_OF_THREADS = config['conf'].getint('number_of_threads')
print(MEDIA_TYPE,MEDIA_QUALITY,DOWNLOAD_MODE)

task_queue = Queue()

def getUrl(task_queue):
    prev_url = None
    while True:
        current_url = pyperclip.paste()
        if(prev_url != current_url):
            if current_url.startswith('https://www.youtube.com/watch?v=') and len(current_url.split("=")) > 1:
                task_queue.put(current_url)
                prev_url = current_url

def task(task_queue,thread_name):
    while True:
        url = task_queue.get()
        try:
            if(MEDIA_TYPE == 'audio'):
                start_audio_download(url)
                task_queue.task_done()
                logging.debug(thread_name+ " Completed")
            elif(MEDIA_TYPE == 'video'):
                if(MEDIA_QUALITY == 'normal'):
                    start_video_download(url)
                    task_queue.task_done()
                    logging.debug(thread_name+ " Completed")
                elif(MEDIA_QUALITY == 'hq'):
                    start_high_quality_video_download(url)
                    task_queue.task_done()
                    logging.debug(thread_name+ " Completed")
            if(task_queue.empty()):
                logging.debug("No pending task in the queue")
        except Exception as e:
            logging.debug("Error occured in daemon loop")

# mainThread
mainThread = Thread(target=getUrl,args=(task_queue,))

worker_thread_list = []
for i in range(NUMBER_OF_THREADS):
    t = Thread(target=task,args=(task_queue,f'Thread-{i}'))
    t.setDaemon(True)
    # t.start()
    worker_thread_list.append(t)

def startTheServer():
    #starting main thread
    mainThread.start()
    #starting worker threads
    for t in worker_thread_list:
        t.start()


if __name__ == '__main__':
    startTheServer()