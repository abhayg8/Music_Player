#Some processing for the GUI

from mutagen.mp3 import MP3 
from mutagen.id3 import ID3
from mutagen.id3._util import ID3NoHeaderError
from PIL import Image
from io import BytesIO
from math import floor

def findSongLength(currentPlaying):
    audio = MP3(currentPlaying)
    audioInfo = audio.info 
    lengthSec = int(audioInfo.length)
    timeStamp = str(floor(lengthSec/60)) + ":" + str(lengthSec%60)
    return timeStamp

def getSongImage(currentPlaying):
    try:
        tags = ID3(currentPlaying)
        photo = tags.get("APIC:").data
        image = Image.open(BytesIO(photo))
        return image
    except ID3NoHeaderError: 
        image = Image.open("C:/Users/abhay/Documents/Projects/Music_Player/images/default.jpg")
        return image



