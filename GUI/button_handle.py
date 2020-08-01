##Button handlers for main window

import tkinter as tk
from pygame import mixer


#Button handlers
def handle_play(event):
    global isPlaying
    if isPlaying:
        mixer.music.unpause()
    else:
        mixer.music.play()
    isPlaying = True

def handle_rewind(event):
    mixer.music.rewind()

def handle_select(event):
    global currentPlaying, currentPlayingLabel, isPlaying, selectLabel
    fileSelected = tk.filedialog.askopenfilename(initialdir="/Users/abhay/Documents/Projects/Music_Player/Sample",filetypes=(("MP3 Files", "*.mp3"),("WAV Files","*.wav")))
    currentPlaying = "./../Sample/sample1.mp3"
    currentPlayingLabel.set(currentPlaying)
    isPlaying = False
    mixer.music.load(currentPlaying)

def set_volume(value):
    volume = int(value)/100
    mixer.music.set_volume(volume)

def handle_pause(event):
    mixer.music.pause()

