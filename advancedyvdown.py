import os
import sys
import pafy # need to download this package explicitly
import pyperclip # need to download this package explicitly
import subprocess
import time

DOWN_DIR='downloads'
LOG_FILE = '.'

#getting audio stream object from pafy
def get_pafy_stream_obj(url):
	try:
		video = pafy.new(url)
		stream_obj = video.getbestaudio(preftype='m4a')
		return stream_obj
	except Exception as e:
		print("Error occured in new pafy")
		return None

def start_download(url):
	try:
		# video = pafy.new(url)
		# stream_obj = video.getbestaudio(preftype='m4a')
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
	if not os.path.exists(path_to_download):
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
		url = sys.argv[1] if len(sys.argv) >1 else None

	if url == None:
		print("No link provided in any means. Not in clipboard not even in as an argument")
		sys.exit()
	start_download(url)