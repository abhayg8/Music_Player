#Main GUI window and interactions go here

import tkinter.filedialog
import tkinter as tk
from pygame import mixer
from button_handle import *


#global variables
isPlaying = False
currentPlaying = "./../Sample/sample1.mp3"

def handle_select(event):
    global currentPlaying, currentPlayingLabel, isPlaying, selectLabel
    fileSelected = tk.filedialog.askopenfilename(initialdir="/Users/abhay/Documents/Projects/Music_Player/Sample",filetypes=(("MP3 Files", "*.mp3"),("WAV Files","*.wav")))
    currentPlaying = fileSelected
    currentPlayingLabel.set(currentPlaying)
    isPlaying = False
    mixer.music.load(currentPlaying)

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

selectFrame = tk.Frame(master=window, relief=tk.GROOVE, width=300, height=50, borderwidth=5)
selectFrame.place(x=100,y=0)


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

selectButton = tk.Button(master=selectFrame,text="Choose song", width=11, height=2)
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




window.mainloop()