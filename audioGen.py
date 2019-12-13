###############
# Taken from here: https://thehackerdiary.wordpress.com/2017/06/09/it-is-ridiculously-easy-to-generate-any-audio-signal-using-python/
###############

# import struct
# import numpy as np
# from scipy import signal as sg

# sampling_rate = 44100
# freq = 440
# samples = 44100
# x = np.arange(samples)

# y = 100*np.sin(2 * np.pi * freq * x / sampling_rate)

# f = open('test.wav', 'wb')

# for i in y:
#     f.write(struct.pack('b', int(i)))
# f.close()


## -------------------------------------------------------------------------------------------------------------------------- ##

## This works fine to generate tones

# import sys
# import wave
# import math
# import struct
# import random
# import argparse
# from itertools import *

# import time 

# def sine_wave(frequency=440.0, framerate=44100, amplitude=0.5):
#     period = int(framerate / frequency)
#     if amplitude > 1.0: amplitude = 1.0
#     if amplitude < 0.0: amplitude = 0.0
#     lookup_table = [float(amplitude) * math.sin(2.0*math.pi*float(frequency)*(float(i%period)/float(framerate))) for i in range(period)]
#     return (lookup_table[i%period] for i in count(0))


# while (True):

#     # print((("Hey")
#     sine_wave(440.0)
#     # time.sleep(10)


# -----------

# import pyttsx3
# engine = pyttsx3.init()
# def onStart(name):
#    print(( 'starting', name)
# def onWord(name, location, length):
#    print(( 'word', name, location, length)
# def onEnd(name, completed):
#    print(( 'finishing', name, completed)
#    if name == 'fox':
#       engine.say('What a lazy dog!', 'dog')
#    elif name == 'dog':
#       engine.endLoop()
# engine = pyttsx3.init()
# engine.connect('started-utterance', onStart)
# engine.connect('started-word', onWord)
# engine.connect('finished-utterance', onEnd)
# engine.say('The quick brown fox jumped over the lazy dog.', 'fox')
# engine.startLoop()

## ----------------------------------

# from pynput.mouse import Listener
# from multiprocessing import Process, Queue

# import cv2
# import numpy as np
# import time

# import pyttsx3

# def play_this(name, engine):

#     engine.say(name)
#     engine.runAndWait()
#     # engine.stop()

# q = Queue() # a mouse movement listener
# c = Queue() # a click listener

# def on_move(x, y):
#     """
#     on mouse movement execute this
#     """
#     # print('Pointer moved to {0}'.format((x, y)))
#     q.put([x, y])

# def on_click(x, y, button, pressed):
#     """
#     on mouse click execute this
#     """
#     # print('{0} at {1}'.format('Pressed' if pressed else 'Released',(x, y)))
#     c.put(pressed)

# # listen asynchronously to the mouse location
# listener = Listener(
#     on_move = on_move,
#     on_click = on_click,
#     args=(q, c),
#     )
# listener.start()

# engine = pyttsx3.init()
# rate = engine.getProperty('rate')
# print("This is the rate: ", rate)


# img = np.zeros((500,500,3), np.uint8)
# cv2.imshow("image", img)

# while(True):
#     cv2.imshow("image", img)
#     while not q.empty():
#         newLocVal = q.get()
#         # print("newLoc Val")

#     # if the mouse is clicked then print return and exit.
#     while not c.empty():
#         if c.get():
#             cv2.destroyAllWindows()
#             print("destroying windows")
#             time.sleep(10)
#             print("MouseClicked.., playing hey yallll")
#             play_this("hey yallll", engine)    


## ------------------------------------------------------

from gtts import gTTS 
import os

def create_audio_files(itemText, saveDir):
    """
    Eg. 
    create_audio_files([lion, buffalo], "audioFiles")
    """

    fPaths = {}
    for i in itemText:
        # remove any whitespace and save in the audiofiles folder 
        compactName = i.replace(" ", "")
        fName = str(compactName + ".mp3") 
        fPath = os.path.join(saveDir, fName)

        # Passing the text and language to the engine,  
        myobj = gTTS(text=i, lang='en', slow=False) 
        myobj.save(fPath) 

        fPaths[compactName] = fPath
    return fPaths

def play_audio(path):
    os.system("mpg321 "+ path)


# # The text that you want to convert to audio 
# mytext = ['lion', 'buffalo', 'gazelle', 'elephant', 'rhino', 'leopard']

# saveDirectory = "audioFiles"
# print(createAudioFiles(mytext, saveDirectory))





