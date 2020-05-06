import os
import requests
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, TIT2, error
from debugger import logging

def addPicture(audio_path,pafy_obj):
    """Add picture to the audio file provided with audio_path arguments
    Picture url will get retrived from the pafy object

    Arguments:
        audio_path {String} -- Path to the audio file to work with
        pafy_obj {Object} -- The pafy object of the current audio file
    Return:
        Doesn't return a value if operations are succeful but if it fail to fetch any image url 
        it return None and no operation is done with the audio file
    """    
    if os.path.exists(audio_path)\
         and os.path.isfile(audio_path)\
              and audio_path.endswith('mp3'):
        if pafy_obj != None:
            audio = MP3(audio_path,ID3=ID3)

            # Download the cover image
            try:
                picture_url = None
                if(pafy_obj.bigthumbhd != None):
                    picture_url = pafy_obj.bigthumbhd
                    logging.debug("BigThumbHd")
                elif(pafy_obj.bigthumb !=None):
                    picture_url = pafy_obj.bigthumb
                    logging.debug("BigThumb")
                elif(pafy_obj.thumb !=None):
                    picture_url = pafy_obj.thumb
                    logging.debug("Thumb")
                else:
                    logging.debug("No thumbnail avaliable for the video")
                    return

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
    """Add metadata title to the audio file provided with audio_path 

    Arguments:
        audio_path {String} -- Path to the audio file
        title {String} -- The title that is going to be added to the audio file
    Return:
        Doesn't return anything
    """    
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
