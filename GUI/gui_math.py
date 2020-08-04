#Some processing for the GUI

from mutagen.mp3 import MP3 
from math import floor

def findSongLength(currentPlaying):
    audio = MP3(currentPlaying)
    audioInfo = audio.info 
    lengthSec = int(audioInfo.length)
    timeStamp = str(floor(lengthSec/60)) + ":" + str(lengthSec%60)
    return timeStamp