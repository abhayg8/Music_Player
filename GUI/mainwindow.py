#Main GUI window and interactions go here

import threading
import pyaudio
import wave
import tkinter.filedialog
import tkinter as tk
from pygame import mixer
from PIL import Image, ImageTk
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
    albumArt = getSongImage(currentPlaying)
    return "break"




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
    nameWindow.configure(bg='black')
    songNameLabel = tk.Label(nameWindow, text="Enter recording name:", width=40, height=7, bg='black', foreground='white')
    songNameLabel.grid(row=0,columnspan=2)
    songNameEntry = tk.Entry(nameWindow)
    songNameEntry.grid(row=1,columnspan=2)
    okButton = tk.Button(nameWindow, text="Save", command=handle_saverec, bg='black', foreground='white')
    okButton.grid(row=2,column=0)
    cancelButton = tk.Button(nameWindow, text="Cancel", command=handle_cancel , bg='black', foreground='white')
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
window.geometry("800x303")
window.title("Epic Digital Audio Workstation")
window.configure(bg='black')

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
play_photo = Image.open("C:/Users/abhay/Documents/Projects/Music_Player/images/play_button.png")
play_photo_resize = play_photo.resize((50,37), Image.ANTIALIAS)
play_photo_tk = ImageTk.PhotoImage(play_photo_resize)

pause_photo = Image.open("C:/Users/abhay/Documents/Projects/Music_Player/images/pause_button.png")
pause_photo_resize = pause_photo.resize((50,37), Image.ANTIALIAS)
pause_photo_tk = ImageTk.PhotoImage(pause_photo_resize)

rewind_photo = Image.open("C:/Users/abhay/Documents/Projects/Music_Player/images/rewind_button.png")
rewind_photo_resize = rewind_photo.resize((50,37), Image.ANTIALIAS)
rewind_photo_tk = ImageTk.PhotoImage(rewind_photo_resize)

record_photo = Image.open("C:/Users/abhay/Documents/Projects/Music_Player/images/record_button.png")
record_photo_resize = record_photo.resize((50,37), Image.ANTIALIAS)
record_photo_tk = ImageTk.PhotoImage(record_photo_resize)

stop_photo = Image.open("C:/Users/abhay/Documents/Projects/Music_Player/images/stop_button.png")
stop_photo_resize = stop_photo.resize((50,37), Image.ANTIALIAS)
stop_photo_tk = ImageTk.PhotoImage(stop_photo_resize)

defAlbumArt = getSongImage(currentPlaying)
defAlbumArt_resize = defAlbumArt.resize((435,238), Image.ANTIALIAS)
defAlbumArt_tk = ImageTk.PhotoImage(defAlbumArt_resize)

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

selectFrame = tk.Frame(master=window, relief=tk.GROOVE, width=300, height=50, borderwidth=5, bg='black')
selectFrame.place(x=100,y=0)

playTimeFrame = tk.Frame(master=window, relief=tk.GROOVE, width=50, height=50, borderwidth=5, bg='black')
playTimeFrame.place(x=665, y=50)

songLengthFrame = tk.Frame(master=window, relief=tk.GROOVE, width=50, height=50, borderwidth=5, bg='black')
songLengthFrame.place(x=665, y=100)

recordFrame = tk.Frame(master=window, relief=tk.GROOVE, width=50, height=50, borderwidth=5)
recordFrame.place(x=100, y=200)

stopRecordFrame = tk.Frame(master=window, relief=tk.GROOVE, width=50, height=50, borderwidth=5)
stopRecordFrame.place(x=100, y=250)

albumArtFrame = tk.Frame(master=window, relief=tk.GROOVE, width=450, height=250, borderwidth=5)
albumArtFrame.place(x=217,y=50)




#Setting up control buttons
playButton = tk.Button(master=playFrame, image=play_photo_tk, width=100, height=37, bg='black')
playButton.pack(side=tk.TOP)
playButton.bind("<Button-1>", handle_play)

pauseButton = tk.Button(master=pauseFrame, image=pause_photo_tk, width=100, height=37, bg='black')
pauseButton.pack(side=tk.TOP)
pauseButton.bind("<Button-1>", handle_pause)

rewindButton = tk.Button(master=rewindFrame, image=rewind_photo_tk, width=100, height=37, bg='black')
rewindButton.pack(side=tk.TOP)
rewindButton.bind("<Button-1>", handle_rewind)

selectButton = tk.Button(master=selectFrame,text="Choose song", width=17, height=2, bg='black', foreground='white')
selectButton.pack(side=tk.LEFT)
selectButton.bind("<Button-1>", handle_select)
selectLabel = tk.Label(selectFrame, textvariable=currentPlayingLabel, width=85, height=2, bg='black', foreground='white')
selectLabel.pack(side=tk.LEFT)

recordButton = tk.Button(master=recordFrame, image=record_photo_tk, width=100, height=37, bg='black')
recordButton.pack(side=tk.TOP)
recordButton.bind("<Button-1>", handle_record)

stopRecordButton = tk.Button(master=stopRecordFrame, image=stop_photo_tk, width=100, height=37, bg='black')
stopRecordButton.pack(side=tk.TOP)
stopRecordButton.bind("<Button-1>", stop_record)

#Setting up volume slider
volumeLabel = tk.Label(volumeFrame, text="    Volume", width=11, height=1, bg='black', foreground='white')
volumeLabel.pack(side=tk.TOP)
volumeSlider = tk.Scale(volumeFrame, from_=100, to=0, width=58, length=264, command = set_volume, bg='black', foreground='black')
volumeSlider.set(50)
volumeSlider.pack(side=tk.TOP)

#Setting up info labels
playTimeInfo = tk.Label(master=playTimeFrame, text="Time Elapsed:", width=10, height=2, bg='black', foreground='white')
playTimeInfo.pack(side=tk.LEFT)
playTimeLabel = tk.Label(master=playTimeFrame, textvariable=playTimeLabelText, width=6, height=1, bg='black', foreground='white')
playTimeLabel.pack(side=tk.RIGHT)

songLengthInfo = tk.Label(master=songLengthFrame, text="Song Length:", width=10, height=2, bg='black', foreground='white')
songLengthInfo.pack(side=tk.LEFT)
songLengthLabel = tk.Label(master=songLengthFrame, textvariable=songLengthLabelText, width=6, height=1, bg='black', foreground='white')
songLengthLabel.pack(side=tk.RIGHT)

#Album Art
albumArtLabel= tk.Label(master=albumArtFrame, image=defAlbumArt_tk, width=435, height=237, bg='black')
albumArtLabel.pack(side=tk.TOP)

playButton.after(1000,duration_control)
window.mainloop()