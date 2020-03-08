# YoutubeDownloader
Download audio or video from YouTube.

## Single File Download at a Time
For downloading a single file at a time copy the youtube url u want to download and either
run `python advancedyvdown.py` it will fetch copied link from clipboard or else give the link
as an argument during runing the script like this: `python advancedyvdown.py -l [Link of the Youtube Video]`

`usage: advancedyvdown.py [-h] [-l LINK] [-v] [-hq]`

Download youtube files either in video or in audio format. By default audio will be
downloaded if argument -v not given.

optional arguments:
  -h, --help            show this help message and exit
  -l LINK, --link LINK  Link of the youtube video to download
  -v, --video           Download in video format.
  -hq, --highquality    Download video in high quality this option is depended on '-v' argument
  
## Youtube Playlist Download
To download a youtube playlist use `main.py` script like this `python main.py`
and provide the link when it is asked by the program.
It will ask if download will be in audio format or in video choose a/v as per the operation 
u like to do.
