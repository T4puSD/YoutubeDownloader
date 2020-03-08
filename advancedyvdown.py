import os
import sys
import pafy # need to download this package explicitly
import pyperclip # need to download this package explicitly
import subprocess
import time
import argparse
import logging
from title_slugify import TitleSlugify

# Static Variables
DOWN_DIR_AUDIO=os.path.join('.','downloads')
DOWN_DIR_VIDEO=os.path.join('.','video_downloads')
TEMP_DIR = os.path.join('.','temp')
LOG_FILE = os.path.join('.','log.txt')
FFMPEG_LOG = '-loglevel'
FFMPEG_LOG_LEVEL = 'warning'

# Setting up logger
# filename=LOG_FILE
logging.basicConfig(filename=LOG_FILE,
					level=logging.DEBUG,
					format = "%(asctime)s:%(levelname)s:%(message)s"
					)



def get_pafy_stream_obj(url,format='AUDIO',only_video=False):
    """This function return stream object from pafy

    Arguments:
            url {string} -- The url of the video from youtube

    Returns:
            Stream_Obj -- This is a object of Stream class from pafy
    """
    try:
        video = pafy.new(url)
        stream_obj = None
        if format == 'AUDIO':
            logging.debug("Getting audio pafy stream_object")
            stream_obj = video.getbestaudio(preftype='m4a')
        if format == 'VIDEO':
            if only_video:
                # get only video at 1080p
                # stream_obj = video.getbestvideo(preftype='mp4')

                ## iterating from backward as best streams are there and
                ## slecting best 1920x1080p mp4 stream
                logging.debug("Getting HQ video pafy stream_object")
                for stream in video.videostreams[::-1]:
                    if stream.extension == 'mp4':
                        if stream.dimensions[0] == 1920 and stream.dimensions[1] == 1080:
                            stream_obj = stream
                            break
            else:
                # get best will return both audio and video normaly at 640p
                logging.debug("Getting normal-video pafy stream_object")
                stream_obj = video.getbest(preftype='mp4')
        return stream_obj
    except Exception as e:
        logging.debug("Error occured in new pafy")
        logging.debug(e)
        return None

def high_quality_video_download(url):
    """ This function download both video and audio separately
        and combine them to produce 1080p video.

        Arguments:
            url {string} -- The url of the video from youtube
    """
    logging.debug("Initiating - {}".format(high_quality_video_download.__name__))
    # making temp directory if not exist
    # this folder will be used to temporary storing video and audio files
    # those temporary files will be deleted once combine operatoin is successfull
    if not os.path.exists(TEMP_DIR):
        try:
            logging.debug("Making {} Directory".format(TEMP_DIR))
            os.mkdir(TEMP_DIR)
       	except Exception as e:
            logging.debug("Error occured in making Directory {}".format(TEMP_DIR))
            logging.debug(e)

    # downloading only audio
    audio = None
    while audio == None:
        audio = get_pafy_stream_obj(url)
        time.sleep(1)

    # slugifying title
    slugify_audio_title = TitleSlugify().slugify_for_windows(audio.title+'.'+audio.extension)
    # setting download location
    temp_path_to_download_audio = os.path.join(TEMP_DIR,slugify_audio_title)

    try:
        logging.debug("Downloading HQ Audio: "+TitleSlugify().slugify_for_windows(audio.title))
        ## print statement
        print("Downloading HQ Video: "+TitleSlugify().slugify_for_windows(audio.title))
        audio.download(filepath=temp_path_to_download_audio)
    except Exception as e:
        logging.debug("Exception occured at high_quality_video_download audio downloader")
        logging.debug(e)


    # downloaing only video
    video = None
    while video == None:
        video = get_pafy_stream_obj(url,format='VIDEO',only_video=True)
        time.sleep(1)
    # slugifying title
    slugify_video_title = TitleSlugify().slugify_for_windows(video.title+'.'+video.extension)
    temp_path_to_download_video = os.path.join(TEMP_DIR,slugify_video_title)

    try:
        logging.debug("Downloading HQ Video: "+TitleSlugify().slugify_for_windows(video.title))
        video.download(filepath=temp_path_to_download_video)
    except Exception as e:
        logging.debug("Exception occured at high_quality_video_download video downloader")
        logging.debug(e)

    output_path = os.path.join(DOWN_DIR_VIDEO,slugify_video_title)
    # combining both video and audio
    cmd = ['ffmpeg',FFMPEG_LOG,FFMPEG_LOG_LEVEL,'-i',temp_path_to_download_video,'-i',temp_path_to_download_audio,'-c','copy','-strict','experimental',output_path]

    # running command with subprocess
    try:
        logging.debug("Combining HQ Audio and Video: "+TitleSlugify().slugify_for_windows(audio.title))
        subprocess.run(cmd)
    except Exception as e:
        logging.debug("Errore occured during runing combining ffmpeg command")
        logging.debug(e)
    finally:
        try:
            os.remove(temp_path_to_download_audio)
            os.remove(temp_path_to_download_video)
        except Exception as e:
            logging.debug("Unable to remove temporary files in temp folder")
            logging.debug(e)




def start_video_download(url):
    """This function download 640p quality normal video.

     Arguments:
            url {string} -- The url of the video from youtube
    """
    logging.debug("Initiating - {}".format(start_video_download.__name__))
    try:
        stream_obj = None
        while(stream_obj == None):
            stream_obj = get_pafy_stream_obj(url,format='VIDEO')
            time.sleep(1)
        # slugify title
        slugify_video_title = TitleSlugify().slugify_for_windows(stream_obj.title+'.'+stream_obj.extension)
        path_to_download = os.path.join(DOWN_DIR_VIDEO,slugify_video_title)
    except Exception as e:
        logging.debug("Error occured in new pafy")
        logging.debug(e)
        sys.exit()

    if not os.path.exists(path_to_download):
        #starting download
        try:
            if not os.path.exists(DOWN_DIR_VIDEO):
                try:
                    logging.debug("Making {} Directory".format(DOWN_DIR_VIDEO))
                    os.mkdir(DOWN_DIR_VIDEO)
                except Exception as e:
                    logging.debug("Error occured in making Directory {}".format(TEMP_DIR))
                    logging.debug(e)
            logging.debug("Downloading Video: "+TitleSlugify().slugify_for_windows(stream_obj.title))
            ## print statement
            print("Downloading Video: "+TitleSlugify().slugify_for_windows(stream_obj.title))
            stream_obj.download(filepath=path_to_download)
        except Exception as e:
            logging.debug("Unable to download. Error occured")
            logging.debug(e)
    else:
        logging.debug("File already exist")


def start_audio_download(url):
    """This is a function to download audio file as m4a form pafy streamobj and also convert them to mp3

    Arguments:
            url {string} -- The url of the video from yoututbe
    """
    logging.debug("Initiating - {}".format(start_audio_download.__name__))
    try:
        # video = pafy.new(url)
        # stream_obj = video.getbestaudio(preftype='m4a')

        # trying to get stream obj from pafy
        # until the object is received witout an errore
        # the while loop keeps reqesting pafy
        stream_obj = None
        while(stream_obj == None):
            stream_obj = get_pafy_stream_obj(url,format='AUDIO')
            time.sleep(1)
        # slugifying title
        slugify_audio_title = TitleSlugify().slugify_for_windows(stream_obj.title+'.'+stream_obj.extension)
        path_to_download = os.path.join(DOWN_DIR_AUDIO, slugify_audio_title)
        # logging.debug(path_to_download)
        # path_to_download = os.path.join(DOWN_DIR_AUDIO,stream_obj.title+'.'+stream_obj.extension)

    except Exception as e:
        logging.debug("Error occured in new pafy")
        logging.debug(e)
        sys.exit()

    #checking if the file already exists
    if not os.path.exists(path_to_download) and not os.path.exists(path_to_download.replace('.m4a','.mp3')):
        #starting download
        try:
            if not os.path.exists(DOWN_DIR_AUDIO):
                try:
                    logging.debug("Making {} Directory".format(DOWN_DIR_AUDIO))
                    os.mkdir(DOWN_DIR_AUDIO)
                except Exception as e:
                    logging.debug("Error occured in making Directory {}".format(DOWN_DIR_AUDIO))
                    logging.debug(e)
            logging.debug("Downloading Audio: "+TitleSlugify().slugify_for_windows(stream_obj.title))
            ## print statement
            print("Downloading Audio: "+TitleSlugify().slugify_for_windows(stream_obj.title))
            stream_obj.download(filepath=path_to_download)
        except Exception as e:
            logging.debug("Unable to download. Error occured")
            logging.debug(e)

        #converting to mp3
        cmd = ['ffmpeg',FFMPEG_LOG,FFMPEG_LOG_LEVEL,'-i',path_to_download,'-vn','-ab','128k','-ar','44100','-y',os.path.join(DOWN_DIR_AUDIO,slugify_audio_title.replace('.m4a','.mp3'))]
        # logging.debug(" ".join(cmd))
        try:
            subprocess.run(cmd)
        except Exception as e:
            logging.debug("Errore occured in converting file")
            logging.debug(e)

        try:
            # subprocess.run(['rm',path_to_download])
            os.remove(path_to_download)
        except Exception as e:
            logging.debug("Errore removing actual file")
            logging.debug(e)
    else:
        logging.debug("File already exists")


# this code will only run if it is executed directly
# if this module is imported from another program the code chunk below won't execute
if __name__ == "__main__":
    #adding argument parser option
    parser = argparse.ArgumentParser(description='Download youtube files either in video or in audio format. By default audio will be downloaded if argument -v not given.')
    parser.add_argument('-l','--link',type=str,help='Link of the youtube video to download')
    parser.add_argument('-v','--video',action='store_true',help='Download in video format.')
    parser.add_argument('-hq','--highquality',action='store_true',help="Download video in high quality this option is depended on '-v' argument")
    # parser.add_argument('-a','--audio',action='store_true',help='Download in audio format.')
    args = parser.parse_args()

    if args.link:
        # logging.debug('link provide   '+args.link)
        if args.link.startswith('https://www.youtube.com/watch?v='):
            if args.video:
                if args.highquality:
                    high_quality_video_download(args.link)
                else:
                    start_video_download(args.link)
            else:
                start_audio_download(args.link)
        else:
            logging.debug("Link provided is not valid")
    else:
        url = pyperclip.paste() if len(pyperclip.paste()) > 10 \
        and pyperclip.paste().startswith('https://www.youtube.com/watch?v=') else None
        if url != None:
            if args.video:
                if args.highquality:
                    high_quality_video_download(url)
                else:
                    start_video_download(url)
            else:
                start_audio_download(url)
        else:
            logging.debug('No link found in the clipboard')
            sys.exit()



    # checking for links in cipboard or in sys argument
    # url = pyperclip.paste() if len(pyperclip.paste()) > 10 \
    # and pyperclip.paste().startswith('https://www.youtube.com/watch?v=') else None

    # if url == None:
    #       url = sys.argv[1] if len(sys.argv) >1 and sys.argv[1].startswith('https://www.youtube.com/watch?v=') else None

    # if url == None:
    #       logging.debug("No link provided in any means. Not in clipboard not even in as an argument")
    #       sys.exit()
    # start_audio_download(url)
