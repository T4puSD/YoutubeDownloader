import os
import requests
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, TIT2, error
from debugger import logging

def addPicture(audio_path,picture_url):
    if os.path.exists(audio_path)\
         and os.path.isfile(audio_path)\
              and audio_path.endswith('mp3'):
        if picture_url != None:
            audio = MP3(audio_path,ID3=ID3)

            # Download the cover image
            try:
                img = requests.get(picture_url)
                # extracting byte data from img response obj
                img = img.content
            except Exception as e:
                logging.debug("Error downloading cover art")
                logging.debug(e)
        
            # try adding id3 tags if not exists
            try:
                audio.add_tags()
            except error:
                logging.debug("ID3 Tag already exists for this audio file")
            
            # editing the id3 tag
            try:
                audio.tags.add(APIC(mime='image/jpeg',type=3,desc=u'Cover',data = img))
                audio.save()
                logging.debug("Cover added")
            except error:
                logging.debug("Error adding coverart")
        else:
            logging.debug("Image path is invalid")
    else:
        logging.debug("audio path is invalid")

def addTitle(audio_path,title):
    if os.path.exists(audio_path):
        if(title!="" or title!=None):
            audio = MP3(audio_path,ID3=ID3)
            try:
                audio.add_tags()
            except error:
                logging.debug("ID3 Tag already exists for this audio file")
            
            try:
                audio.tags.add(TIT2(encoding=3,text=title))
                audio.save()
                logging.debug("Title  Added")
            except error:
                logging.debug("Error Adding Title to audio file")
        else:
            logging.debug("Title can't be null or empty")
    else:
        logging.debug("audio path is invalid")
