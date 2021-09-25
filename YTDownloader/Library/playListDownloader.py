import concurrent.futures
from YTDownloader.Library.getuList import SongListGenerator
from YTDownloader.debugger import logging
from YTDownloader.advancedyvdown import start_audio_download, start_video_download

#url = 'https://www.youtube.com/playlist?list=PLRiSVT9MWtYwyhhgVNnRDTpCRvF-t2lc8'
url = input("Enter a valid YouTube  Playlist Link:")
while not url.startswith('https://www.youtube.com/playlist?list'):
	url = input("Enter a valid YouTube  Playlist Link:")

av = ['a','v']
aud_or_vid = None
while not aud_or_vid in av:
	aud_or_vid = input("Download in audio or video (a/v)?")
song_list = SongListGenerator().generateList(url)

song_batchs_of_three = [song_list[i:i+3] for i in range(0,len(song_list),3)]
# print(song_batchs_of_three)

# print(song_list)
if len(song_list) > 0:
	try:
		if aud_or_vid == av[0]:
			for batch_one in song_batchs_of_three:
				with concurrent.futures.ThreadPoolExecutor() as executor:
					executor.map(start_audio_download,batch_one)
		elif aud_or_vid == av[1]:
			for batch_one in song_batchs_of_three:
				with concurrent.futures.ThreadPoolExecutor() as executor:
					executor.map(start_video_download,batch_one)
	except Exception as e:
		logging.debug("Exception occured running threadpool executor")
		logging.debug(e)