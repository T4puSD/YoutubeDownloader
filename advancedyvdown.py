import os
import sys
import pafy # need to download this package explicitly
import pyperclip # need to download this package explicitly
import subprocess
import time

# Static Variables
DOWN_DIR='downloads'
LOG_FILE = '.'

#getting audio stream object from pafy
"""
This function
"""
def get_pafy_stream_obj(url):
	"""This function return stream object from pafy
	
	Arguments:
		url {string} -- The url of the video from youtube
	
	Returns:
		Stream_Obj -- This is a object of Stream class from pafy
	"""
	try:
		video = pafy.new(url)
		stream_obj = video.getbestaudio(preftype='m4a')
		return stream_obj
	except Exception as e:
		print("Error occured in new pafy")
		return None

def start_download(url):
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
			stream_obj = get_pafy_stream_obj(url)
			time.sleep(1)
		path_to_download = os.path.join(DOWN_DIR,stream_obj.title+'.'+stream_obj.extension)
	except Exception as e:
		print("Error occured in new pafy")
		print(e)
		sys.exit()

	#checking if the file already exists
	if not os.path.exists(path_to_download) and not os.path.exists(path_to_download.replace('.m4a','.mp3')):
		#starting download
		try:
			print("Downloading: "+stream_obj.title)
			stream_obj.download(filepath=path_to_download)
		except Exception as e:
			print("Unable to download. Error occured")
			print(e)

		#converting to mp3
		cmd = ['ffmpeg','-hide_banner','-loglevel','panic','-i',path_to_download,'-vn','-ab','128k','-ar','44100','-y',os.path.join(DOWN_DIR,stream_obj.title+'.'+'mp3')]
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
	# checking for links in cipboard or in sys argument
	url = pyperclip.paste() if len(pyperclip.paste()) > 10 \
	and pyperclip.paste().startswith('https://www.youtube.com/watch?v=') else None

	if url == None:
		url = sys.argv[1] if len(sys.argv) >1 and sys.argv[1].startswith('https://www.youtube.com/watch?v=') else None

	if url == None:
		print("No link provided in any means. Not in clipboard not even in as an argument")
		sys.exit()
	start_download(url)