import concurrent.futures
from getuList import SongListGenerator
from advancedyvdown import start_audio_download, start_video_download, logging

#url = 'https://www.youtube.com/playlist?list=PLRiSVT9MWtYwyhhgVNnRDTpCRvF-t2lc8'
url = input("Enter a valid YouTube  Playlist Link:")
while not url.startswith('https://www.youtube.com/playlist?list'):
	url = input("Enter a valid YouTube  Playlist Link:")

av = ['a','v']
aud_or_vid = None
while not aud_or_vid in av:
	aud_or_vid = input("Download in audio or video (a/v)?")
song_list = SongListGenerator().generateList(url)
# print(song_list)
if len(song_list) > 0:
	try:
		if aud_or_vid == av[0]:
			with concurrent.futures.ThreadPoolExecutor() as executor:
				executor.map(start_audio_download,song_list)
		elif aud_or_vid == av[1]:
			with concurrent.futures.ThreadPoolExecutor() as executor:
				executor.map(start_video_download,song_list)
	except Exception as e:
		logging.debug("Exception occured running threadpool executor")
		logging.debug(e)