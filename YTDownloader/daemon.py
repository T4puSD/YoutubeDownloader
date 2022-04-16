import sys
import signal
import pyperclip
import queue

from YTDownloader import configuration
from YTDownloader.Enums import MediaType, VideoQuality
from YTDownloader.debugger import logging
from YTDownloader.advancedyvdown import start_audio_download
from YTDownloader.advancedyvdown import start_video_download
from YTDownloader.advancedyvdown import start_high_quality_video_download
from YTDownloader.Library.Threading.stoppableThread import StoppableThread

task_queue = queue.Queue()


class ClipBoardThread(StoppableThread):
    def __init__(self, queue, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = queue

    def run(self):
        prev_url = pyperclip.paste()
        while not self.stopped():
            current_url = pyperclip.paste()
            if prev_url != current_url:
                if current_url.startswith('https://www.youtube.com/watch?v=') and len(current_url.split("=")) > 1:
                    self.queue.put(current_url)
                    prev_url = current_url


class WorkerThread(StoppableThread):
    def __init__(self, queue, thread_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.task_queue = queue
        self.thread_name = thread_name

    def run(self):
        config = configuration.get_config()
        while not self.stopped():
            try:
                url = self.task_queue.get(timeout=1)
            except queue.Empty:
                pass
            else:
                try:
                    if config.get_media_type == MediaType.AUDIO:
                        start_audio_download(url)
                        task_queue.task_done()
                        logging.debug(self.thread_name + " Completed")
                    elif config.get_media_type == MediaType.VIDEO:
                        if config.get_media_quality == VideoQuality.Q360P:
                            start_video_download(url)
                            task_queue.task_done()
                            logging.debug(self.thread_name + " Completed")
                        elif config.get_media_quality == VideoQuality.Q1080P:
                            start_high_quality_video_download(url)
                            task_queue.task_done()
                            logging.debug(self.thread_name + " Completed")
                    if task_queue.empty():
                        logging.debug("No pending task in the queue")
                except Exception as e:
                    logging.debug("Error occurred in daemon loop")
                    logging.debug(e)


# mainThread
mainThread = ClipBoardThread(task_queue)

worker_thread_list = []
for i in range(configuration.get_config().get_number_of_threads):
    t = WorkerThread(task_queue, f'Thread-{i}')
    t.daemon = True
    # t.start()
    worker_thread_list.append(t)


def stop_the_servers():
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

            # for worker in worker_thread_list:
            #     # Allow worker threads to shut down completely
            #     worker.join()
    return result


def reset_the_threads():
    # task_queue = queue.Queue()
    global mainThread
    global worker_thread_list
    mainThread = ClipBoardThread(task_queue)
    worker_thread_list.clear()
    for i in range(configuration.get_config().get_number_of_threads):
        t = WorkerThread(task_queue, f'Thread-{i}')
        worker_thread_list.append(t)


def sigint_handler(signum, frame):
    logging.debug('Shutting Threads down...')
    stop_the_servers()
    sys.exit(0)


def start_the_servers():
    config = configuration.get_config()
    logging.debug("Starting Daemon Server! Modes: {} {} {}"
                  .format(config.get_media_type, config.get_media_quality, config.get_download_mode))

    if mainThread.is_alive():
        return True

    if not mainThread.is_alive():
        # starting main thread
        mainThread.start()

    work_is_pending = True
    for worker in worker_thread_list:
        if not worker.is_alive():
            work_is_pending = False
    if not work_is_pending:
        # starting worker threads
        for t in worker_thread_list:
            t.start()
        return False

    # while not task_queue.empty():
    #     time.sleep(0.1)

    # print("stopping main thread")
    # mainThread.stop()
    # print("main thread is stopped")


def main():
    signal.signal(signal.SIGINT, sigint_handler)
    start_the_servers()


if __name__ == '__main__':
    main()
