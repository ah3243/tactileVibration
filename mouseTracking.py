
"""
    The goal of this script is to form the basis of a basic dynamic digital haptic display

    This script
    1. Takes in mouse movement and clicks.
    2. Creates an opencv window and scales the mouse movement to fit inside of it
    3. Randomly generates shapes(bar charts etc)
    4. Returns the color of the pixel that the mouse is currently over

"""

import cv2
import numpy as np

from pynput.mouse import Listener
from multiprocessing import Process, Queue

import random # for random column height generation
import audioGen # to create audio files

# import pyttsx3

q = Queue() # a mouse movement listener
c = Queue() # a click listener

def on_move(x, y):
    """
    on mouse movement execute this
    """
    # print('Pointer moved to {0}'.format((x, y)))
    q.put([x, y])

def on_click(x, y, button, pressed):
    """
    on mouse click execute this
    """
    # print('{0} at {1}'.format('Pressed' if pressed else 'Released',(x, y)))
    c.put(True)

# listen asynchronously to the mouse location
listener = Listener(
    on_move = on_move,
    on_click = on_click,
    args=(q, c),
    )
listener.start()

# engine = pyttsx3.init()
# # set the engine property to 400 (originally 200)
# rate = engine.getProperty('rate')   # getting details of current speaking rate
# engine.setProperty('rate', 400)     # setting up new voice rate

def sayLabel(name, engine):
    pass
    # say whatever text is sent to it

    # engine.stop()

def isObject(x, y, img):
    """
    Read the pixel BGR value for the pointers current location
    """
    print(x, y, "  and color: ", img[x,y])
    return img[x,y]

screenDims = (800, 1280) # the dimensions of my laptop screen
imgDims = (500, 640, 3) # the dimensions of the opencv window (y, x, channels)

# scaleFactor = (0.4, 0.64) # the scaling factors to convert the screen location to opencv window location
scaleFactor = (imgDims[0]/screenDims[0], imgDims[1]/screenDims[1]) # the scaling factors to convert the screen location to opencv window location

def drawMyCircle(imgCpy, circleLoc):
    """
    Draw a small point to mimic the movement of the mouse
    """
    circleSize = 2
    circleStroke = -1
    circleColor = (255,255,0)

    cv2.circle(imgCpy, circleLoc, circleSize+2, (0,0,0), circleStroke) # create a black outline for the new pointer dot
    cv2.circle(imgCpy, circleLoc, circleSize, circleColor, circleStroke) # create a turquoise central point for the new pointer dot

def findColorKey(imgDets, color):
    """
    This function matches a color with it's label in the dictionary
    """

    # if the color is black return False
    blackColor = [0,0,0]
    if (color == blackColor).all():
        print("black has been clicked on..")
        return False

    # create a list of the bar details key and values 
    keys = list(imgDets["barDetails"].keys())
    values = list(imgDets["barDetails"].values())
    
    # search for the colors corresponding label
    cnter = 0
    for tarVal in values:

        if (color == tarVal).all():
            print("This is the color: ", color, " and associated label: ", keys[cnter])
            return keys[cnter]
        cnter+=1

    return False

def drawMyBarChart(imgCpy, imgDets):
    """
    draw randomly generated vertical coloumns
    """

    # calculate the gap between columns and their x locations
    imgXSize= imgCpy.shape[1]
    gapBetweenCols = 30
    numCols = len(imgDets["colHeights"]) # find the number of cols
    colWidth = int( (imgXSize-((numCols+1)*gapBetweenCols))/numCols ) # calculate the column width based on the number of cols etc
    recStroke = -1   

    cntX = gapBetweenCols

    # Create a list of the bar colors
    colorList = list(imgDets["barDetails"].values())

    # cycle through the bar heights and colors, drawing them on the image
    for i in range(len(imgDets["colHeights"])):
        recTopLeft = (cntX, imgDets["colHeights"][i]) # (x, y)
        cntX+=colWidth
        recBotRight = (cntX, imgCpy.shape[0])
        cv2.rectangle(imgCpy, recTopLeft, recBotRight, colorList[i], recStroke)
        cntX +=gapBetweenCols

newLocVal = [0,0] # placeholder for get

barDetails = {"Elephant" : (255,0,0), "Lion": (0, 255, 0), "Rhino": (0, 0, 255), "Buffalo": (0,255,255), \
    "Leopard": (255,255,0), "Gazelle": (255,0,255)}
col_heights = []

# generate a list of random column heights (within the image height)
for e in range(len(barDetails)):
    col_heights.append(random.randint(1, imgDims[0]))

# dictionary holding column values
imgDetails = {
    "barDetails": barDetails,
    "colHeights": col_heights
    }

while(True):
    # generate a new matrix
    img = np.zeros(imgDims, np.uint8)

    # draw the graphic(bar chart) being explored in this program to the new matrix
    drawMyBarChart(img, imgDetails)

    # get the current mouse location from the other thread(and cycle through until only the most current is left)
    while not q.empty():
        newLocVal = q.get()

    # calculate the new circle point adjusted for the different screen size. 
    ## Note: mouse values are switched compared to scale x,y vals to switched back for calculation
    newCircleLoc = (int(newLocVal[0]*scaleFactor[1]), int(newLocVal[1]*scaleFactor[0]))

    # if the mouse is clicked then print return and exit.
    while not c.empty():
        mouseClicked = c.get()

        # get the color that the mouse is over
        currentMColor = isObject(newCircleLoc[1], newCircleLoc[0], img)

        # get the colors associated label
        mouseColor = findColorKey(imgDetails, currentMColor)
        if mouseColor is not False:
            sayLabel(mouseColor)

            # engine.say(mouseColor)
            # engine.runAndWait()
            # print("This is mouseColor")


    # if not newCircleLoc[0]>imgDims[0] or newCircleLoc[1]>imgDims[1]:
    drawMyCircle(img, newCircleLoc)

    cv2.imshow("imgWindow", img)
    cv2.moveWindow("imgWindow", 400, 50)

    k = cv2.waitKey(100) & 0xFF
    if k == ord('q'):
        print("q pressed. Exiting..")
        # cv2.destroyAllWindows()
        # exit()




