from getuList import SongListGenerator
from advancedyvdown import start_download

url = 'https://www.youtube.com/playlist?list=PLRiSVT9MWtYwyhhgVNnRDTpCRvF-t2lc8'
song_list = SongListGenerator().generateList(url)
print(song_list)
if len(song_list) > 0:
	for song_url in song_list:
		start_download(song_url)