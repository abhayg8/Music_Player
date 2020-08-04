#Main GUI window and interactions go here

import tkinter.filedialog
import tkinter as tk
from pygame import mixer
from gui_math import *
import time
from math import floor



#global variables
newSong = True
isPlaying = False
currentPlaying = "./../Sample/sample1.mp3"
currentSaveDir = "./../temp_save"
songLength = "--:--"

#Button handlers
def handle_play(event):
    global isPlaying, newSong, songLengthLabelText, currentPlaying
    if isPlaying:
        mixer.music.unpause()
    else:
        mixer.music.play()
        songLengthLabelText.set(findSongLength(currentPlaying))
    isPlaying = True
    newSong = False
    

def handle_rewind(event):
    global currentPlaying, newSong
    mixer.music.stop()
    mixer.music.load(currentPlaying)
    mixer.music.play()

def handle_select(event):
    global currentPlaying, currentPlayingLabel, isPlaying, selectLabel, playTimeLabelText, newSong, songLengthLabelText
    fileSelected = tk.filedialog.askopenfilename(initialdir="/Users/abhay/Documents/Projects/Music_Player/Sample",filetypes=(("MP3 Files", "*.mp3"),("WAV Files","*.wav")))
    currentPlaying = fileSelected
    currentPlayingLabel.set(fileSelected)
    isPlaying = False
    newSong = True
    mixer.music.load(currentPlaying)
    songLength = findSongLength(currentPlaying)
    songLengthLabelText.set(songLength)

def handle_savedir(event):
    global currentSaveDir, currentSaveDirLabel
    dirSelected = tk.filedialog.askdirectory()
    currentSaveDir = dirSelected
    currentSaveDirLabel.set(dirSelected)



def set_volume(value):
    volume = int(value)/100
    mixer.music.set_volume(volume)

def handle_pause(event):
    mixer.music.pause()

def duration_control():
    global playTimeLabelText, newSong
    lengthSec=0
    lengthMin=0
    lengthMilli = mixer.music.get_pos()
    if lengthMilli!=0:
       lengthSec = floor(lengthMilli/1000)
       lengthSecRemain = lengthSec%60
       lengthMin = floor(lengthSec/60)
    else:
        lengthSec = 0
        lengthSecRemain = 0
        lengthMin = 0
    playingDuration = str(lengthMin) + ":" + str(lengthSecRemain)

    if not newSong:
        playTimeLabelText.set(playingDuration)
    else: 
        playTimeLabelText.set("--:--")
    playButton.after(1000,duration_control)

      



##Initialising pygame mixer
mixer.init()
mixer.music.load(currentPlaying)
mixer.music.set_volume(0.5)

#Setting up window for program
window  = tk.Tk()
window.geometry("800x500")
window.title("Epic Digital Audio Workstation")

#Setting up song label 
currentPlayingLabel = tk.StringVar()
currentPlayingLabel.set("./../Sample/sample1.mp3")
currentSaveDirLabel = tk.StringVar()
currentSaveDirLabel.set("./../temp_save")
playTimeLabelText = tk.StringVar()
playTimeLabelText.set("--:--")
songLengthLabelText = tk.StringVar()
songLengthLabelText.set("--:--")


#Generating images for buttons 
play_photo = tk.PhotoImage(file="C:/Users/abhay\Documents/Projects/Music_Player/images/play_button.png")

#Used to calibrate the size of pixels in buttons
pixelVirtual = tk.PhotoImage(width=1,height=1)

#Frames in the home window
volumeFrame = tk.Frame(master=window, relief=tk.GROOVE,  width=100, height=350, borderwidth=5)
volumeFrame.place(x=0,y=0)

playFrame = tk.Frame(master=window, relief=tk.GROOVE, width=100, height=50, borderwidth=5)
playFrame.place(x=0,y=350)

pauseFrame = tk.Frame(master=window, relief=tk.GROOVE, width=100, height=50, borderwidth=5)
pauseFrame.place(x=0,y=400)

rewindFrame = tk.Frame(master=window, relief=tk.GROOVE, width=100, height=50, borderwidth=5)
rewindFrame.place(x=0,y=450)

saveDirFrame = tk.Frame(master=window, relief=tk.GROOVE, width=300, height=50, borderwidth=5)
saveDirFrame.place(x=100,y=0)

selectFrame = tk.Frame(master=window, relief=tk.GROOVE, width=300, height=50, borderwidth=5)
selectFrame.place(x=100,y=50)

playTimeFrame = tk.Frame(master=window, relief=tk.GROOVE, width=50, height=50, borderwidth=5)
playTimeFrame.place(x=100, y=350)

songLengthFrame = tk.Frame(master=window, relief=tk.GROOVE, width=50, height=50, borderwidth=5)
songLengthFrame.place(x=100, y=425)




#Setting up control buttons
playButton = tk.Button(master=playFrame,text="Play", width=11, height=2)
playButton.pack()
playButton.bind("<Button-1>", handle_play)

pauseButton = tk.Button(master=pauseFrame,text="Pause", width=11, height=2)
pauseButton.pack()
pauseButton.bind("<Button-1>", handle_pause)

rewindButton = tk.Button(master=rewindFrame,text="Rewind", width=11, height=2)
rewindButton.pack()
rewindButton.bind("<Button-1>", handle_rewind)

saveDirButton = tk.Button(master=saveDirFrame,text="Choose save directory", width=17, height=2)
saveDirButton.pack(side=tk.LEFT)
saveDirButton.bind("<Button-1>", handle_savedir)
saveDirLabel = tk.Label(saveDirFrame, textvariable=currentSaveDirLabel, width=85, height=2)
saveDirLabel.pack(side=tk.LEFT)

selectButton = tk.Button(master=selectFrame,text="Choose song", width=17, height=2)
selectButton.pack(side=tk.LEFT)
selectButton.bind("<Button-1>", handle_select)
selectLabel = tk.Label(selectFrame, textvariable=currentPlayingLabel, width=85, height=2)
selectLabel.pack(side=tk.LEFT)

#Setting up volume slider
volumeLabel = tk.Label(volumeFrame, text="    Volume", width=11, height=1)
volumeLabel.pack(side=tk.TOP)
volumeSlider = tk.Scale(volumeFrame, from_=100, to=0, width=58, length=313, command = set_volume)
volumeSlider.set(50)
volumeSlider.pack(side=tk.TOP)

#Setting up info labels
playTimeInfo = tk.Label(master=playTimeFrame, text="Time Elapsed:", width=11, height=4)
playTimeInfo.pack(side=tk.LEFT)
playTimeLabel = tk.Label(master=playTimeFrame, textvariable=playTimeLabelText, width=8, height=1)
playTimeLabel.pack(side=tk.RIGHT)

songLengthInfo = tk.Label(master=songLengthFrame, text="Song Length:", width=11, height=4)
songLengthInfo.pack(side=tk.LEFT)
songLengthLabel = tk.Label(master=songLengthFrame, textvariable=songLengthLabelText, width=8, height=1)
songLengthLabel.pack(side=tk.RIGHT)

playButton.after(1000,duration_control)
window.mainloop()