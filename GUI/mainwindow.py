#Main GUI window and interactions go here

import tkinter as tk
from pygame import mixer

#global variables
isPlaying = False

#Button handlers
def handle_play(event):
    global isPlaying
    if isPlaying:
        mixer.music.unpause()
    else:
        mixer.music.play()
    isPlaying = True

def handle_pause(event):
    mixer.music.pause()

def handle_rewind(event):
    mixer.music.rewind()

def set_volume(value):
    volume = int(value)/100
    mixer.music.set_volume(volume)


##Initialising pygame mixer
mixer.init()
mixer.music.load("./../Sample/sample1.mp3")

#Setting up window for program
window  = tk.Tk()
window.geometry("1000x500")
window.title("Epic Digital Audio Workstation")

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

playButton = tk.Button(master=playFrame,text="Play", width=11, height=2)
playButton.pack()
playButton.bind("<Button-1>", handle_play)

pauseButton = tk.Button(master=pauseFrame,text="Pause", width=11, height=2)
pauseButton.pack()
pauseButton.bind("<Button-1>", handle_pause)

rewindButton = tk.Button(master=rewindFrame,text="Rewind", width=11, height=2)
rewindButton.pack()
rewindButton.bind("<Button-1>", handle_rewind)

volumeLabel = tk.Label(volumeFrame, text="    Volume", width=11, height=1)
volumeLabel.pack(side=tk.TOP)
volumeSlider = tk.Scale(volumeFrame, from_=100, to=0, width=58, length=313, command = set_volume)
volumeSlider.pack(side=tk.TOP)



window.mainloop()