import matplotlib.pyplot as plt
import numpy as np
import pylab
import sys
import datetime
import getopt
import os
import subprocess

def splitvideos():
    splitPoints.sort()
    print splitPoints
    videoDir = os.path.dirname(videoFile)
    parentPath = os.getcwd()
    programPath = os.path.join(parentPath, 'SplitClips')
    print programPath

    gestures = ('thumb','index','middle','ring','pinky','fist')
    numGestPerformed = 5

    if videoDir != '':
        os.chdir(videoDir)

    currentGesture = 0
    currentIteration = 0

    if not os.path.exists(gestures[0]):
        os.mkdir(gestures[0])

    for i in range(len(splitPoints) - 1):
        if currentIteration == numGestPerformed:
            currentGesture += 1
            currentIteration = 0
            if not os.path.exists(gestures[currentGesture]):
                os.mkdir(gestures[currentGesture])
        print "split : ", splitPoints[i], splitPoints[i+1]

        filename = gestures[currentGesture] + str(currentIteration) + '.avi'
        outfile = os.path.join(videoDir, gestures[currentGesture], filename)
        print 'output: ', outfile

        currentIteration += 1
        subprocess.call([programPath, videoFile, str(splitPoints[i]), str(splitPoints[i+1]), outfile])



def onclick(event):
    global initX, initY
    
    initX = event.xdata
    initY = event.ydata

def onrelease(event):
    global initX, initY
    print 'xdata=%f'%(
        event.xdata)

    if initX == event.xdata and initY == event.ydata:
        #circ = plt.Circle((event.xdata, event.ydata), radius=2, color='g')
        #ax1.add_patch(circ)
        ln = plt.plot([event.xdata, event.xdata], [1000, -1000], color='k', linestyle='-', linewidth=2)
        #number of frames per video segment is 250 (50frames * 5s)
        #range to 250*numClips
        #assuming only 10 clips.. 2500
        for i in xrange(0,2500,250):
            ln = plt.plot([event.xdata+i, event.xdata+i], [1000, -1000], color='k', linestyle='-', linewidth=2)
        fig.canvas.draw()
        splitPoints.append(int(round(initX)))
        splitLines.append(ln)

def press(event):
    global cid, toggleClick
    #print('press', event.key)
    sys.stdout.flush()

    if event.key == 'w':
        splitvideos()
        exit()
    if event.key == 'u':
        splitPoints.pop()
        ln, = splitLines.pop()
        ln.remove()
        fig.canvas.draw()
    if event.key == 'q':
        exit()
    # toggle click
    if event.key == ' ':
        if toggleClick:
            cid = fig.canvas.mpl_connect('button_press_event', onclick)
            print 'point selection mode on'
            toggleClick = False
        else:
            fig.canvas.mpl_disconnect(cid)
            print 'navigation mode on'
            toggleClick = True

videoFile = sys.argv[1] 

toggleClick = False

splitPoints = []
splitLines = []

data = pylab.loadtxt("graph2.txt")

fig = plt.figure()
cid = fig.canvas.mpl_connect('button_press_event', onclick)
rid = fig.canvas.mpl_connect('button_release_event', onrelease)
pid = fig.canvas.mpl_connect('key_press_event', press)

ax1 = fig.add_subplot(111)

ax1.plot(data)
plt.show()

