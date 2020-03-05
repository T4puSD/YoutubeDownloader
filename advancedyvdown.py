import os
import sys
import pafy # need to download this package explicitly
import pyperclip # need to download this package explicitly
import subprocess
import time
import argparse

# Static Variables
DOWN_DIR_AUDIO='downloads'
DOWN_DIR_VIDEO='video_downloads'
LOG_FILE = '.'


def get_pafy_stream_obj(url,format='AUDIO'):
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
            stream_obj = video.getbestaudio(preftype='m4a')
        if format == 'VIDEO':
            stream_obj = video.getbestvideo(preftype='mp4')
        return stream_obj
    except:
        print("Error occured in new pafy")
        return None

def start_video_download(url):
    try:
        stream_obj = None
        while(stream_obj == None):
            stream_obj = get_pafy_stream_obj(url,format='VIDEO')
            time.sleep(1)
        path_to_download = os.path.join(DOWN_DIR_VIDEO,stream_obj.title+'.'+stream_obj.extension)
    except Exception as e:
        print("Error occured in new pafy")
        print(e)
        sys.exit()

    if not os.path.exists(path_to_download):
    	#starting download
        try:
            if not os.path.exists(os.path.join('.',DOWN_DIR_VIDEO)):
                os.mkdir(os.path.join('.',DOWN_DIR_VIDEO))
            print("Downloading Video: "+stream_obj.title)
            stream_obj.download(filepath=path_to_download)
        except Exception as e:
            print("Unable to download. Error occured")
            print(e)



def start_audio_download(url):
    """This is a function to download audio file as m4a form pafy streamobj and also convert them to mp3

    Arguments:
            url {string} -- The url of the video from yoututbe
    """
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
        path_to_download = os.path.join(DOWN_DIR_AUDIO,stream_obj.title+'.'+stream_obj.extension)
    except Exception as e:
        print("Error occured in new pafy")
        print(e)
        sys.exit()

    #checking if the file already exists
    if not os.path.exists(path_to_download) and not os.path.exists(path_to_download.replace('.m4a','.mp3')):
        #starting download
        try:
            if not os.path.exists(os.path.join('.',DOWN_DIR_AUDIO)):
                os.mkdir(os.path.join('.',DOWN_DIR_AUDIO))
            print("Downloading Audio: "+stream_obj.title)
            stream_obj.download(filepath=path_to_download)
        except Exception as e:
            print("Unable to download. Error occured")
            print(e)

        #converting to mp3
        cmd = ['ffmpeg','-hide_banner','-loglevel','panic','-i',path_to_download,'-vn','-ab','128k','-ar','44100','-y',os.path.join(DOWN_DIR_AUDIO,stream_obj.title+'.'+'mp3')]
        # print(cmd)
        try:
            subprocess.run(cmd)
        except Exception as e:
            print("Errore occured in converting file")
            print(e)

        try:
            # subprocess.run(['rm',path_to_download])
            os.remove(path_to_download)
        except Exception as e:
            print("Errore removing actual file")
            print(e)
    else:
        print("File already exists")


# this code will only run if it is executed directly
# if this module is imported from another program the code chunk below won't execute
if __name__ == "__main__":
	#adding argument parser option
	parser = argparse.ArgumentParser(description='Download youtube files either in video or in audio format.')
	parser.add_argument('-l','--link',type=str,help='Link of the youtube video to download')
	parser.add_argument('-v','--video',action='store_true',help='Download in video format.')
	parser.add_argument('-a','--audio',action='store_true',help='Download in audio format.')
	args = parser.parse_args()

	format = None
	if args.video:
		format = 'VIDEO'
	if args.audio:
		format = 'AUDIO'
	if args.link:
		# print('link provide   '+args.link)
		if args.link.startswith('https://www.youtube.com/watch?v='):
			if args.audio:
				start_audio_download(args.link)
			if args.video:
				start_video_download(args.link)
		else:
			print("Link provided is not valid")
	else:
		url = pyperclip.paste() if len(pyperclip.paste()) > 10 \
		and pyperclip.paste().startswith('https://www.youtube.com/watch?v=') else None
		if url != None:
			if args.video:
				start_video_download(url)
			else:
				start_audio_download(url)
		else:
			print('No link found in the clipboard')
			sys.exit()



    # checking for links in cipboard or in sys argument
    # url = pyperclip.paste() if len(pyperclip.paste()) > 10 \
    # and pyperclip.paste().startswith('https://www.youtube.com/watch?v=') else None

    # if url == None:
    #       url = sys.argv[1] if len(sys.argv) >1 and sys.argv[1].startswith('https://www.youtube.com/watch?v=') else None

    # if url == None:
    #       print("No link provided in any means. Not in clipboard not even in as an argument")
    #       sys.exit()
    # start_audio_download(url)
