import os
import sys
import pyperclip
import subprocess
import argparse
from YTDownloader.debugger import logging
from YTDownloader.Configuration.configuration import get_configuration
from YTDownloader.Library.title_slugify import TitleSlugify
from YTDownloader.Library.notifier import notifyAboutTheService
from YTDownloader.Library.ffmpeg_path import FfmpegPath
from YTDownloader.Library.pafy_handler import FormatType, get_pafy_obj
from YTDownloader.Library.Media.AudioFile import AudioFile

# load basic Configuration files
config = get_configuration()
# Static Variables
DOWN_DIR_AUDIO = config.get_download_dir_audio
DOWN_DIR_VIDEO = config.get_download_dir_video
TEMP_DIR = config.get_temporary_directory
FFMPEG_LOG = '-loglevel'
FFMPEG_LOG_LEVEL = 'warning'
FFMPEG_LOCATION = FfmpegPath.getFFmpegExecutablePath()


def reloadDownloadDirs():
    global DOWN_DIR_AUDIO
    global DOWN_DIR_VIDEO

    config = get_configuration()

    DOWN_DIR_AUDIO = config.get_download_dir_audio
    DOWN_DIR_VIDEO = config.get_download_dir_video


def start_high_quality_video_download(url):
    """ This function download both video and audio separately
        and combine them to produce 1080p video.

        Arguments:
            url {string} -- The url of the video from youtube
    """
    logging.debug("Initiating - {}".format(start_high_quality_video_download.__name__))
    # making temp directory if not exist
    # this folder will be used to temporary storing video and audio files
    # those temporary files will be deleted once combine operation is successful
    if not os.path.exists(TEMP_DIR):
        try:
            logging.debug("Making Directory: {}".format(TEMP_DIR))
            os.makedirs(TEMP_DIR)
        except Exception as e:
            logging.debug("Error occurred in making Directory: {}".format(TEMP_DIR))
            logging.debug(e)

    if not os.path.exists(DOWN_DIR_VIDEO):
        try:
            logging.debug("Making Directory: {}".format(DOWN_DIR_VIDEO))
            os.makedirs(DOWN_DIR_VIDEO)
        except Exception as e:
            logging.debug("Error occurred in making Directory: {}".format(DOWN_DIR_VIDEO))
            logging.debug(e)

    # downloading only video
    video = get_pafy_obj(url, FormatType.VIDEO, only_video=True)
    if video is not None:
        # normalizing title
        slugify_video_title = TitleSlugify().slugify_for_windows(video.title + '.' + video.extension)
        temp_path_to_download_video = os.path.join(TEMP_DIR, slugify_video_title)

        output_path = os.path.join(DOWN_DIR_VIDEO, slugify_video_title)
        if not os.path.exists(output_path):
            try:
                logging.debug("Downloading HQ Video: " + TitleSlugify().slugify_for_windows(video.title))
                video.download(filepath=temp_path_to_download_video)
            except Exception as e:
                logging.debug("Exception occurred at high_quality_video_download video downloader")
                logging.debug(e)
                # this need to be checked
                return

            # downloading only audio
            audio = get_pafy_obj(url, FormatType.AUDIO)

            # if audio is not available
            # then video is also not available
            if audio is not None:
                # Normalizing title
                slugify_audio_title = TitleSlugify().slugify_for_windows(audio.title + '.' + audio.extension)
                # setting download location
                temp_path_to_download_audio = os.path.join(TEMP_DIR, slugify_audio_title)

                try:
                    logging.debug("Downloading HQ Audio: " + TitleSlugify().slugify_for_windows(audio.title))
                    audio.download(filepath=temp_path_to_download_audio)
                except Exception as e:
                    logging.debug("Exception occurred at high_quality_video_download audio downloader")
                    logging.debug(e)

                # combining both video and audio
                cmd = [str(FFMPEG_LOCATION), FFMPEG_LOG, FFMPEG_LOG_LEVEL, '-i', temp_path_to_download_video, '-i',
                       temp_path_to_download_audio, '-c', 'copy', '-strict', 'experimental', output_path]

                # running command with subprocess
                try:
                    logging.debug("Combining HQ Audio and Video: " + TitleSlugify().slugify_for_windows(audio.title))
                    logging.debug("Saving to: " + os.path.abspath(DOWN_DIR_VIDEO))
                    subprocess.run(cmd, shell=True)
                    logging.debug("DOWNLOADED=> " + slugify_video_title)
                    notifyAboutTheService("Downloaded", slugify_video_title)

                except Exception as e:
                    notifyAboutTheService("Error Downloading", slugify_video_title)
                    logging.debug("Error occurred during running combining ffmpeg command")
                    logging.debug(e)
                finally:
                    try:
                        os.remove(temp_path_to_download_audio)
                        os.remove(temp_path_to_download_video)
                    except Exception as e:
                        logging.debug("Unable to remove temporary files in temp folder({})".format(TEMP_DIR))
                        logging.debug(e)
        else:
            logging.debug("File Already Exists! Path: " + output_path)
    else:
        logging.debug("Unable to find the video file at this time. Timeout!! Try again later.")


def start_video_download(url):
    """This function download 640p quality normal video.

     Arguments:
            url {string} -- The url of the video from youtube
    """
    logging.debug("Initiating - {}".format(start_video_download.__name__))

    stream_obj = get_pafy_obj(url, FormatType.VIDEO)

    if stream_obj is not None:
        # slugify title
        slugify_video_title = TitleSlugify().slugify_for_windows(stream_obj.title + '.' + stream_obj.extension)
        path_to_download = os.path.join(DOWN_DIR_VIDEO, slugify_video_title)

        if not os.path.exists(path_to_download):
            # starting download
            try:
                if not os.path.exists(DOWN_DIR_VIDEO):
                    try:
                        logging.debug("Making Directory: {}".format(DOWN_DIR_VIDEO))
                        os.makedirs(DOWN_DIR_VIDEO)
                        # os.mkdir(DOWN_DIR_VIDEO)
                    except Exception as e:
                        logging.debug("Error occurred in making Directory: {}".format(TEMP_DIR))
                        logging.debug(e)
                logging.debug("Downloading Video: " + TitleSlugify().slugify_for_windows(stream_obj.title))
                logging.debug("Saving to: " + os.path.abspath(DOWN_DIR_VIDEO))
                stream_obj.download(filepath=path_to_download)
                logging.debug("DOWNLOADED=> " + slugify_video_title)
                notifyAboutTheService("Downloaded", slugify_video_title)
            except Exception as e:
                notifyAboutTheService("Error Downloading", slugify_video_title)
                logging.debug("Unable to download. Error occurred")
                logging.debug(e)
        else:
            logging.debug("File Already Exists! Path: " + path_to_download)
    else:
        logging.debug("Unable to find the video file at this time. Timeout!! Try again later.")


def start_audio_download(url):
    """This is a function to download audio file as m4a form pafy stream obj and also convert them to mp3

    Arguments:
            url {string} -- The url of the video from YouTube
    """
    logging.debug("Initiating - {}".format(start_audio_download.__name__))

    try:
        AudioFile(get_pafy_obj(url)).start_download()
    except Exception as ex:
        logging.debug(start_audio_download.__name__ + "- Exception: " + ex.__str__())


# this code will only run if it is executed directly
# if this module is imported from another program the code chunk below won't execute
if __name__ == "__main__":
    # adding argument parser option
    parser = argparse.ArgumentParser(
        description="""Download youtube files either in video or in audio format. By default audio will be downloaded
                    if argument -v not given.""")
    parser.add_argument('-l', '--link', type=str, help='Link of the youtube video to download')
    parser.add_argument('-v', '--video', action='store_true', help='Download in video format.')
    parser.add_argument('-hq', '--highquality', action='store_true',
                        help="Download video in high quality. This option is depended on '-v' argument.")
    # parser.add_argument('-a','--audio',action='store_true',help='Download in audio format.')
    args = parser.parse_args()

    if args.link:
        # logging.debug('link provide   '+args.link)
        if args.link.startswith('https://www.youtube.com/watch?v='):
            if args.video:
                if args.highquality:
                    start_high_quality_video_download(args.link)
                else:
                    start_video_download(args.link)
            else:
                start_audio_download(args.link)
        else:
            logging.debug("Link provided is not valid")
    else:
        url = pyperclip.paste() if len(pyperclip.paste()) > 10 \
                                   and pyperclip.paste().startswith('https://www.youtube.com/watch?v=') else None
        if url is not None:
            if args.video:
                if args.highquality:
                    start_high_quality_video_download(url)
                else:
                    start_video_download(url)
            else:
                start_audio_download(url)
        else:
            logging.debug('No link found in the clipboard')
            sys.exit()
