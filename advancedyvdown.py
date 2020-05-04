import os
import sys
import pafy # need to download this package explicitly
import pyperclip # need to download this package explicitly
import subprocess
import json
import time
import argparse
# import logging
from debugger import logging
from configparser import ConfigParser
from config import generateConfigFile
from title_slugify import TitleSlugify
from notifier import notifyAboutTheService
from metaDataEditor import addTitle, addPicture


# genererating configure.json file at first to
# load basic config files
if not os.path.exists(os.path.join('.','configure.ini')):
    generateConfigFile()
if os.path.exists(os.path.join('.','configure.ini')):
    config = ConfigParser()
    config.read('configure.ini')

# Static Variables
# * is used to unpack from list
DOWN_DIR_AUDIO=os.path.join(*config['conf'].get('download_dir_audio').split(',')) # downloads
DOWN_DIR_VIDEO=os.path.join(*config['conf'].get('download_dir_video').split(','))
TEMP_DIR = os.path.join(*config['conf'].get('temp_dir').split(','))
FFMPEG_LOG = '-loglevel'
FFMPEG_LOG_LEVEL = 'warning'

def get_pafy_stream_obj(url,format=None,only_video=False):
    """This function return stream object from pafy

    Arguments:
            url {string} -- The url of the video from youtube

    Returns:
            Stream_Obj -- This is a object of Stream class from pafy
    """
    try:
        obj = pafy.new(url)
        # returning only the pafy obj if format is not given
        if format == None:
            return obj
        
        stream_obj = None
        # returning format specified in the parameter
        if format == 'AUDIO':
            logging.debug("Getting audio pafy stream_object")
            stream_obj = obj.getbestaudio(preftype='m4a')
        if format == 'VIDEO':
            if only_video:
                # get only video at 1080p
                # stream_obj = obj.getbestvideo(preftype='mp4')

                ## iterating from backward as best streams are there and
                ## slecting best 1920x1080p mp4 stream
                logging.debug("Getting HQ video pafy stream_object")
                for stream in obj.videostreams[::-1]:
                    if stream.extension == 'mp4':
                        if stream.dimensions[0] == 1920 and stream.dimensions[1] == 1080:
                            stream_obj = stream
                            break
            else:
                # get best will return both audio and obj normaly at 640p
                logging.debug("Getting normal-video pafy stream_object")
                stream_obj = obj.getbest(preftype='mp4')
        return stream_obj

    except OSError as e:
        logging.debug("OSError in new pafy")
        logging.debug(e)
        raise OSError
    except Exception as e:
        logging.debug("Error occured in new pafy")
        logging.debug(e)
        return None

def start_high_quality_video_download(url):
    """ This function download both video and audio separately
        and combine them to produce 1080p video.

        Arguments:
            url {string} -- The url of the video from youtube
    """
    logging.debug("Initiating - {}".format(start_high_quality_video_download.__name__))
    # making temp directory if not exist
    # this folder will be used to temporary storing video and audio files
    # those temporary files will be deleted once combine operatoin is successfull
    if not os.path.exists(TEMP_DIR):
        try:
            logging.debug("Making {} Directory".format(TEMP_DIR))
            os.makedirs(TEMP_DIR)
        except Exception as e:
            logging.debug("Error occured in making Directory {}".format(TEMP_DIR))
            logging.debug(e)

    if not os.path.exists(DOWN_DIR_VIDEO):
        try:
            logging.debug("Making {} Directory".format(DOWN_DIR_VIDEO))
            os.makedirs(DOWN_DIR_VIDEO)
        except Exception as e:
            logging.debug("Error occured in making Directory {}".format(DOWN_DIR_VIDEO))
            logging.debug(e)


    # downloaing only video
    timeout = 5
    video = None
    while video == None and timeout>0:
        try:
            video = get_pafy_stream_obj(url,format='VIDEO',only_video=True)
            time.sleep(1)
        except OSError:
            logging.debug("Video is not available in Youtube.")
            logging.debug("Link: "+url)
            break
        timeout-=1
    
    if video is not None:
        # slugifying title
        slugify_video_title = TitleSlugify().slugify_for_windows(video.title+'.'+video.extension)
        temp_path_to_download_video = os.path.join(TEMP_DIR,slugify_video_title)

        output_path = os.path.join(DOWN_DIR_VIDEO,slugify_video_title)
        if not os.path.exists(output_path):
            try:
                logging.debug("Downloading HQ Video: "+TitleSlugify().slugify_for_windows(video.title))
                video.download(filepath=temp_path_to_download_video)
            except Exception as e:
                logging.debug("Exception occured at high_quality_video_download video downloader")
                logging.debug(e)
                # this need to be checked
                return

            # downloading only audio
            timeout = 5
            audio = None
            while audio == None and timeout>0:
                try:
                    audio = get_pafy_stream_obj(url,format='AUDIO')
                    time.sleep(1)
                except OSError:
                    logging.debug("Video is not availble in Youtube.")
                    logging.debug("Link: "+ url)
                    break
                timeout-=1
            # if audio is not avilable 
            # then video is also not available
            if audio is not None:
                # slugifying title
                slugify_audio_title = TitleSlugify().slugify_for_windows(audio.title+'.'+audio.extension)
                # setting download location
                temp_path_to_download_audio = os.path.join(TEMP_DIR,slugify_audio_title)

                try:
                    logging.debug("Downloading HQ Audio: "+TitleSlugify().slugify_for_windows(audio.title))
                    audio.download(filepath=temp_path_to_download_audio)
                except Exception as e:
                    logging.debug("Exception occured at high_quality_video_download audio downloader")
                    logging.debug(e)


                # combining both video and audio
                cmd = ['ffmpeg',FFMPEG_LOG,FFMPEG_LOG_LEVEL,'-i',temp_path_to_download_video,'-i',temp_path_to_download_audio,'-c','copy','-strict','experimental',output_path]

                # running command with subprocess
                try:
                    logging.debug("Combining HQ Audio and Video: "+TitleSlugify().slugify_for_windows(audio.title))
                    logging.debug("Saving to: "+os.path.abspath(DOWN_DIR_VIDEO))
                    subprocess.run(cmd)
                    logging.debug("DOWNLOADED=> "+slugify_video_title)
                    notifyAboutTheService("Downloaded",slugify_video_title)

                except Exception as e:
                    notifyAboutTheService("Error Downloading",slugify_video_title)
                    logging.debug("Errore occured during runing combining ffmpeg command")
                    logging.debug(e)
                finally:
                    try:
                        os.remove(temp_path_to_download_audio)
                        os.remove(temp_path_to_download_video)
                    except Exception as e:
                        logging.debug("Unable to remove temporary files in temp folder({})".format(TEMP_DIR))
                        logging.debug(e)
        else:
            logging.debug("File Already Exists! Path: "+output_path)
    else:
        logging.debug("Unable to find the video file at this time. Timeout!! Try again later.")




def start_video_download(url):
    """This function download 640p quality normal video.

     Arguments:
            url {string} -- The url of the video from youtube
    """
    logging.debug("Initiating - {}".format(start_video_download.__name__))

    timeout = 5
    stream_obj = None
    while(stream_obj == None and timeout > 0):
        try:
            stream_obj = get_pafy_stream_obj(url,format='VIDEO')
            time.sleep(1)
            timeout-=1
        except OSError:
            logging.debug("Video is not available in Youtube.")
            logging.debug("Link: "+url)
            break
        except Exception as e:
            logging.debug("Error occured in new pafy")
            logging.debug(e)

    if stream_obj is not None:
         # slugify title
        slugify_video_title = TitleSlugify().slugify_for_windows(stream_obj.title+'.'+stream_obj.extension)
        path_to_download = os.path.join(DOWN_DIR_VIDEO,slugify_video_title)

        if not os.path.exists(path_to_download):
            #starting download
            try:
                if not os.path.exists(DOWN_DIR_VIDEO):
                    try:
                        logging.debug("Making {} Directory".format(DOWN_DIR_VIDEO))
                        os.makedirs(DOWN_DIR_VIDEO)
                        # os.mkdir(DOWN_DIR_VIDEO)
                    except Exception as e:
                        logging.debug("Error occured in making Directory {}".format(TEMP_DIR))
                        logging.debug(e)
                logging.debug("Downloading Video: "+TitleSlugify().slugify_for_windows(stream_obj.title))
                logging.debug("Saving to: "+os.path.abspath(DOWN_DIR_VIDEO))
                stream_obj.download(filepath=path_to_download)
                logging.debug("DOWNLOADED=> "+slugify_video_title)
                notifyAboutTheService("Downloded",slugify_video_title)
            except Exception as e:
                notifyAboutTheService("Error Downloading",slugify_video_title)
                logging.debug("Unable to download. Error occured")
                logging.debug(e)
        else:
            logging.debug("File Already Exists! Path: "+path_to_download)
    else:
        logging.debug("Unable to find the video file at this time. Timeout!! Try again later.")


def start_audio_download(url):
    """This is a function to download audio file as m4a form pafy streamobj and also convert them to mp3

    Arguments:
            url {string} -- The url of the video from yoututbe
    """
    logging.debug("Initiating - {}".format(start_audio_download.__name__))
        # trying to get stream obj from pafy
        # until the object is received witout an errore
        # the while loop keeps reqesting pafy
        # if video is not available in youtube
        # gives OSError and breaks the loop
    timeout = 5
    stream_obj = None
    while(stream_obj == None and timeout >0):
        try:
            pafy_obj = get_pafy_stream_obj(url)
            time.sleep(1)
            timeout-=1
        except OSError:
            logging.debug("Video is not available in Youtube.")
            logging.debug("Link: "+url)
            break
        except Exception as e:
            logging.debug("Error occured in new pafy")
            logging.debug(e)
            # sys.exit()
    if pafy_obj is not None:
        # getting audio streams from pafy_obj
        stream_obj = pafy_obj.getbestaudio(preftype='m4a')
        # slugifying title
        slugify_audio_title = TitleSlugify().slugify_for_windows(stream_obj.title+'.'+stream_obj.extension)
        path_to_download = os.path.join(DOWN_DIR_AUDIO, slugify_audio_title)

        #checking if the file already exists
        if not os.path.exists(path_to_download) and not os.path.exists(path_to_download.replace('.m4a','.mp3')):
            #starting download
            try:
                if not os.path.exists(DOWN_DIR_AUDIO):
                    try:
                        logging.debug("Making {} Directory".format(DOWN_DIR_AUDIO))
                        os.makedirs(DOWN_DIR_AUDIO)
                        # os.mkdir(DOWN_DIR_AUDIO)
                    except Exception as e:
                        logging.debug("Error occured in making Directory {}".format(DOWN_DIR_AUDIO))
                        logging.debug(e)

                logging.debug("Downloading Audio: "+TitleSlugify().slugify_for_windows(stream_obj.title))
                # intiate the download
                stream_obj.download(filepath=path_to_download)
                logging.debug("Saving to: "+os.path.abspath(DOWN_DIR_AUDIO))

                #converting to mp3
                cmd = ['ffmpeg',FFMPEG_LOG,FFMPEG_LOG_LEVEL,'-i',path_to_download,'-vn','-ab','128k','-ar','44100','-y',os.path.join(DOWN_DIR_AUDIO,slugify_audio_title.replace('.m4a','.mp3'))]
                # logging.debug(" ".join(cmd))
                try:
                    subprocess.run(cmd)
                    logging.debug("DOWNLOADED=> "+slugify_audio_title.replace("m4a","mp3"))
                    # adding unicode title from stream obj
                    addTitle(path_to_download.replace('m4a','mp3'),stream_obj.title)
                    addPicture(path_to_download.replace('m4a','mp3'),pafy_obj.thumb)
                    notifyAboutTheService("Downloaded",slugify_audio_title.replace("m4a","mp3"))
                except Exception as e:
                    notifyAboutTheService("Error Downloading",slugify_audio_title.replace("m4a","mp3"))
                    logging.debug("Errore occured in converting file")
                    logging.debug(e)

                try:
                    # subprocess.run(['rm',path_to_download])
                    os.remove(path_to_download)
                except Exception as e:
                    logging.debug("Errore removing actual file")
                    logging.debug(e)

            except Exception as e:
                logging.debug("Unable to download. Error occured")
                logging.debug(e)
        else:
            logging.debug("File Already Exists! Path: "+path_to_download)
    else:
        logging.debug("Unable to find the audio file at this time. Timeout!! Try again later.")


# this code will only run if it is executed directly
# if this module is imported from another program the code chunk below won't execute
if __name__ == "__main__":
    #adding argument parser option
    parser = argparse.ArgumentParser(description='Download youtube files either in video or in audio format. By default audio will be downloaded if argument -v not given.')
    parser.add_argument('-l','--link',type=str,help='Link of the youtube video to download')
    parser.add_argument('-v','--video',action='store_true',help='Download in video format.')
    parser.add_argument('-hq','--highquality',action='store_true',help="Download video in high quality. This option is depended on '-v' argument.")
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
        if url != None:
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
