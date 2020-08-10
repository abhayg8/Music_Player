#Main GUI window and interactions go here

import threading
import pyaudio
import wave
import tkinter.filedialog
import tkinter as tk
from pygame import mixer
from gui_math import *
import time
from math import floor



#global variables
newSong = True
isPlaying = False
isRecording = False
currentPlaying = "./../Sample/sample1.mp3"
songLength = "--:--"
saveFile = ''
nameWindow = None

#PyAudio variables
chunk = 1024 
sampleFormat = pyaudio.paInt16 
channels = 2
fs = 44100 
pyaud = pyaudio.PyAudio()
streamGlob = None
frames = []

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

def handle_record(event):
    global isRecording, chunk, sampleFormat, fs, channels, pyaud, streamGlob
    isRecording=True

    streamGlob = pyaud.open(format=sampleFormat,channels=channels,rate=fs,frames_per_buffer=chunk,input=True)
    thread = threading.Thread(target=record_loop)
    thread.start()
      
def record_loop():
    global isRecording, streamGlob, frames, chunk
    while isRecording:
        data = streamGlob.read(chunk)
        frames.append(data)
def stop_record(event):
    global isRecording, frames, channels, sampleFormat, fs, pyaud, streamGlob, saveFile, nameWindow, songNameEntry
    isRecording = False

    nameWindow = tk. Tk()
    nameWindow.geometry("300x300")
    nameWindow.title("Epic DAW")
    songNameLabel = tk.Label(nameWindow, text="Enter recording name:", width=40, height=7)
    songNameLabel.grid(row=0,columnspan=2)
    songNameEntry = tk.Entry(nameWindow)
    songNameEntry.grid(row=1,columnspan=2)
    okButton = tk.Button(nameWindow, text="Save", command=handle_saverec)
    okButton.grid(row=2,column=0)
    cancelButton = tk.Button(nameWindow, text="Cancel", command=handle_cancel)
    cancelButton.grid(row=2, column=1)

def handle_saverec():
    global nameWindow, frames, channels, sampleFormat, fs, pyaud, streamGlob, songNameEntry
    
    songName = songNameEntry.get()
    filepath = "./../Recordings/" + songName + ".wav"
    print(filepath)
    nameWindow.destroy()

    #Making the wave file
    wavFile = wave.open(filepath, 'wb')
    wavFile.setnchannels(channels)
    wavFile.setsampwidth(pyaud.get_sample_size(sampleFormat))
    wavFile.setframerate(fs)
    wavFile.writeframes(b''.join(frames))
    wavFile.close()
    frames = []
    pyaud.close(streamGlob)

def handle_cancel():
    global frames, nameWindow

    frames = []
    nameWindow.destroy()



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
playFrame.place(x=100,y=50)

pauseFrame = tk.Frame(master=window, relief=tk.GROOVE, width=100, height=50, borderwidth=5)
pauseFrame.place(x=100,y=100)

rewindFrame = tk.Frame(master=window, relief=tk.GROOVE, width=100, height=50, borderwidth=5)
rewindFrame.place(x=100,y=150)

selectFrame = tk.Frame(master=window, relief=tk.GROOVE, width=300, height=50, borderwidth=5)
selectFrame.place(x=100,y=0)

playTimeFrame = tk.Frame(master=window, relief=tk.GROOVE, width=50, height=50, borderwidth=5)
playTimeFrame.place(x=665, y=50)

songLengthFrame = tk.Frame(master=window, relief=tk.GROOVE, width=50, height=50, borderwidth=5)
songLengthFrame.place(x=665, y=100)

recordFrame = tk.Frame(master=window, relief=tk.GROOVE, width=50, height=50, borderwidth=5)
recordFrame.place(x=100, y=200)

stopRecordFrame = tk.Frame(master=window, relief=tk.GROOVE, width=50, height=50, borderwidth=5)
stopRecordFrame.place(x=100, y=250)




#Setting up control buttons
playButton = tk.Button(master=playFrame,text="Play", width=17, height=2)
playButton.pack()
playButton.bind("<Button-1>", handle_play)

pauseButton = tk.Button(master=pauseFrame,text="Pause", width=17, height=2)
pauseButton.pack()
pauseButton.bind("<Button-1>", handle_pause)

rewindButton = tk.Button(master=rewindFrame,text="Rewind", width=17, height=2)
rewindButton.pack()
rewindButton.bind("<Button-1>", handle_rewind)

selectButton = tk.Button(master=selectFrame,text="Choose song", width=17, height=2)
selectButton.pack(side=tk.LEFT)
selectButton.bind("<Button-1>", handle_select)
selectLabel = tk.Label(selectFrame, textvariable=currentPlayingLabel, width=85, height=2)
selectLabel.pack(side=tk.LEFT)

recordButton = tk.Button(master=recordFrame, text="Record", width=17, height=2)
recordButton.pack(side=tk.LEFT)
recordButton.bind("<Button-1>", handle_record)

stopRecordButton = tk.Button(master=stopRecordFrame, text="Stop Record", width=17, height=2)
stopRecordButton.pack(side=tk.LEFT)
stopRecordButton.bind("<Button-1>", stop_record)

#Setting up volume slider
volumeLabel = tk.Label(volumeFrame, text="    Volume", width=11, height=1)
volumeLabel.pack(side=tk.TOP)
volumeSlider = tk.Scale(volumeFrame, from_=100, to=0, width=58, length=264, command = set_volume)
volumeSlider.set(50)
volumeSlider.pack(side=tk.TOP)

#Setting up info labels
playTimeInfo = tk.Label(master=playTimeFrame, text="Time Elapsed:", width=10, height=2)
playTimeInfo.pack(side=tk.LEFT)
playTimeLabel = tk.Label(master=playTimeFrame, textvariable=playTimeLabelText, width=6, height=1)
playTimeLabel.pack(side=tk.RIGHT)

songLengthInfo = tk.Label(master=songLengthFrame, text="Song Length:", width=10, height=2)
songLengthInfo.pack(side=tk.LEFT)
songLengthLabel = tk.Label(master=songLengthFrame, textvariable=songLengthLabelText, width=6, height=1)
songLengthLabel.pack(side=tk.RIGHT)

playButton.after(1000,duration_control)
window.mainloop()