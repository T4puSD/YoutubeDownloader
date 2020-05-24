# YoutubeDownloader
Download audio or video from YouTube.

## Dependencies
 1. [ffmpeg](https://www.ffmpeg.org/download.html)
 2. bs4==0.0.1
 3. notify2==0.3.1
 4. pafy==0.5.5
 5. pyperclip==1.8.0
 6. requests==2.23.0
 7. youtube-dl==2020.3.24
 8. mutagen==1.44.0
 9. pyqt5==5.14.2
 10. win10toast==0.9

 >***NOTE:** ffmpeg needed to be installed explicitly and also in the PATH variable! Click on ffmpeg to go to the official download site.*

## How to use CLI version
Every command follows this pattern:
`python [scriptname.py] [options] [parameter if needed]`
>***NOTE**: Every command specified in this document will only work inside the downloaded repository. So, first run your CMD or Terminal inside the downloaded directory then follow along.*
### Download Server
The `daemon.py` script is responsible for running a download server in background and it will start downloading any video as soons as you copy a YouTube url once started.

To start the server run `python daemon.py` this will start the server in audio download mode. But you can configure the server download mode by editing the `configure.ini` file.
#### Edit server configuration
Frist of all if you don't have the `configure.ini` file in the repository or you messed up the file while editing it, you can always generate the default `configure.ini` file by running `python config.py` comand. It will generate this following configure.ini file. **By default** the configure file is set to download **audio** file.
```ini
[conf]
download_dir_audio = testdownloads3
download_dir_video = testdownloads3,video
temp_dir = temp
log_file = log.txt
download_mode = single
number_of_threads = 2

[media_conf]
media_type = audio
media_quality = normal
```
#### Configure to download Video
Edit `media_type` key from `audio` to `video` to configure the server to download video at **480p**.
Edit `media_quality` key from `normal` to `hq` to configure the server to download video at **1080p**.
>***NOTE**: For `conf` section only keys are case sensitive. But both keys and values are case sensitive for `media_conf`. So use lowercase letters only.*
#### Configure dowload location
As of now download location is relative to the repository directory. So whatever you put on `download_dir_audio` or `download_dir_video` will be created within the repository.
>***NOTE:** To define a subdirectory as a download location use `,` as a seperating delimiter.*
>For example `download_dir_video` key's value `testdowlnoads3,video` means **video** folder inside **testdownoads3** directory.

### Single Download
There is two way you can download a single video first method is:
 1. First copy a YouTube video url from your browser.
 2. Run `python advancedyvdown.py` it will fetch copied link from clipboard and start the download

For the second method you follow step 1 from above and then give the copied link as the argument while  running the script as follows:
    `python advancedyvdown.py -l https://www.youtube.com/watch?v=gUQDq9ezuJQ`
This command will start downloading that video file in **mp3** format.

To download as **mp4** at **480p** file format use the `-v` option. Example:
    `python advancedyvdown.py -v -l https://www.youtube.com/watch?v=gUQDq9ezuJQ`

To download as **mp4** at **1080p** file format use both `-v` and `-hq` option. Example:
    `python advancedyvdown.py -v -hq -l https://www.youtube.com/watch?v=gUQDq9ezuJQ`
>***NOTE**: If you don't provide `-l https://www.youtube.com/watch?v=gUQDq9ezuJQ` this argument the scipt will try to find link in the clipboard and if it doesn't find any youtube link scipt will just exit.*

For any help with the terminal use `python advancedyvdown.py -h` as an argument. This will generate this text:
```sh
usage: advancedyvdown.py [-h] [-l LINK] [-v] [-hq]

Download youtube files either in video or in audio format. By default audio will be
downloaded if argument -v not given.

optional arguments:
-h, --help            show this help message and exit
-l LINK, --link LINK  Link of the youtube video to download
-v, --video           Download in video format.
-hq, --highquality    Download video in high quality this option is depended on '-v' argument
```
### Playlist Download
If you want to download a full public YouTube playlist then follow these steps:

 1. Copy the playlist url from the browser
 2. Then run `python playListDownloader.py`
 
The script will ask for the Playlist url; Paste the url into the terminal and it will ask in which file format you want to downlaod press `a` for downloading in audio format or `v` to download in 480p mp4 file format.