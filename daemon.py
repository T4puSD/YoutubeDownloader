import os
import sys
import signal
import time
import pyperclip
from threading import Thread
import queue
from configparser import ConfigParser
from concurrent.futures import as_completed
from config import generateConfigFile
from debugger import logging
from advancedyvdown import start_audio_download
from advancedyvdown import start_video_download
from advancedyvdown import start_high_quality_video_download
from stoppableThread import StoppableThread

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
# print(MEDIA_TYPE,MEDIA_QUALITY,DOWNLOAD_MODE)

task_queue = queue.Queue()

class ClipBoardThread(StoppableThread):
    def __init__(self, queue, *args,**kwargs):
        super().__init__(*args, **kwargs)
        self.queue = queue
    def run(self):
        prev_url = None
        while not self.stopped():
            current_url = pyperclip.paste()
            if(prev_url != current_url):
                if current_url.startswith('https://www.youtube.com/watch?v=') and len(current_url.split("=")) > 1:
                    self.queue.put(current_url)
                    prev_url = current_url

class WorkerThread(StoppableThread):
    def __init__(self,queue,thread_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.task_queue = queue
        self.thread_name = thread_name
    def run(self):
        while not self.stopped():
            try:
                url = self.task_queue.get(timeout=5)
            except queue.Empty:
                pass
            else:
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
                            logging.debug(self.thread_name+ " Completed")
                    if(task_queue.empty()):
                        logging.debug("No pending task in the queue")
                except Exception as e:
                    logging.debug("Error occured in daemon loop")

# mainThread
mainThread = ClipBoardThread(task_queue)

worker_thread_list = []
for i in range(NUMBER_OF_THREADS):
    t = WorkerThread(task_queue,f'Thread-{i}')
    # t.setDaemon(True)
    # t.start()
    worker_thread_list.append(t)

def stopTheServers():
    result = False
    # checkin if main thread is alive
    if mainThread.is_alive():
        # stopping main thread
        mainThread.stop()
        result = True

        work_is_pending = True
        for worker in worker_thread_list:
            if not worker.is_alive():
                work_is_pending = False
                
        # checking if workers are alive
        if work_is_pending:
            # stopping worker threads
            for worker in worker_thread_list:
                worker.stop()

            for worker in worker_thread_list:
                # Allow worker threads to shut down completely
                worker.join()
    return result

def resetTheThreads():
    # task_queue = queue.Queue()
    global mainThread
    global worker_thread_list
    mainThread = ClipBoardThread(task_queue)
    worker_thread_list.clear()
    for i in range(NUMBER_OF_THREADS):
        t = WorkerThread(task_queue,f'Thread-{i}')
        worker_thread_list.append(t)

def sigint_handler(signum, frame):
    print ('\nShutting down...')
    stopTheServers()
    sys.exit(0)

def startTheServers():
    if mainThread.is_alive():
        return True
    
    print(MEDIA_TYPE,MEDIA_QUALITY,DOWNLOAD_MODE)
    if not mainThread.is_alive():
        #starting main thread
        mainThread.start()
    
    work_is_pending = True
    for worker in worker_thread_list:
        if not worker.is_alive():
            work_is_pending = False
    if not work_is_pending:
        #starting worker threads
        for t in worker_thread_list:
            t.start()
        return False

    # while not task_queue.empty():
    #     time.sleep(0.1)

    # print("stopping main thread")
    # mainThread.stop()
    # print("main thread is stopped")

if __name__ == '__main__':
    signal.signal(signal.SIGINT, sigint_handler)
    startTheServers()