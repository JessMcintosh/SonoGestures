import matplotlib.pyplot as plt
import numpy as np
import pylab
import sys
import os
import csv
import subprocess
import scipy.signal

SAMPLING_FR = 1000.0 / 50.0 #50 FPS


#uniformly resamples the matrix data using data[][0] as the timestamps
# the returned data still contains the timestamp (uniform now) in data[][0]
def resampleUniform(data, samplingPeriod):
    rows = len(data[0])
    columns = len(data)
    
    #r = np.array()
    r = [] 
        
    currentTime = data[0][0]
    startTime = currentTime 
    currentIndex = 0
    iters = 0

    while currentIndex < columns:
        while currentIndex < columns and (currentTime > data[currentIndex][0]):
            currentIndex += 1
        
        if currentIndex < columns-1:
            aTime = data[currentIndex][0]
            bTime = data[currentIndex+1][0]
            pTime = (currentTime - aTime) / (bTime - aTime)
            row = [currentTime]
            for i in range(1, rows):
                currentValue = data[currentIndex][i]
                nextValue = data[currentIndex+1][i]
                interp = currentValue + (nextValue-currentValue)*pTime
                row.append( interp )
            r.append( row )
        currentTime = startTime + iters*samplingPeriod
        iters += 1
    return r


    
def splitSensor(filename, sensorStart, sensorEnd):
    try:
        os.remove(filename)
    except OSError:
        pass
    open(filename, 'a').close()
    with open(filename, 'a') as csvfile: 
        writer = csv.writer(csvfile, delimiter=' ')
                #quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for i in range(sensorStart, sensorEnd):
            sensorValues = []
            for j in range(1,6):
                #sensorValues.append(sensorLine.get_ydata()[i])
                #print i, sensorLine.get_ydata(True)[i]
                sensorValues.append(sensorData[i,j])
                #print i, sensorLine.get_xdata(True)[i]
            writer.writerow(sensorValues)


def splitvideos():
    parentPath = os.path.dirname(sys.argv[0])
    #parentPath = os.getcwd()
    programPath = os.path.join(parentPath, 'build', 'SplitClips')
    videoDir = os.path.dirname(videoFile)

    if videoDir != '':
        os.chdir(videoDir)

    currentGesture = 0
    currentIteration = 0
    extensionNumber = 0

    if not os.path.exists(gestures[0]):
        os.mkdir(gestures[0])

    sensorPos = sensorLines[0].get_xdata()[0]
    #print 'sensor start position', sensorPos

    for line in splitLines[:-1]:
        if currentIteration == numGestPerformed:
            currentGesture += 1
            currentIteration = 0
            if currentGesture > 9:
                extensionNumber = 5
            else:
                extensionNumber = 0
            if not os.path.exists(gestures[currentGesture]):
                os.mkdir(gestures[currentGesture])
        startPoint = line.get_xdata()[0]
        endPoint = startPoint + 250        
        print "split : ", startPoint, endPoint

        vfilename = gestures[currentGesture] + str(extensionNumber) + '.avi'
        sfilename = gestures[currentGesture] + str(extensionNumber) + '.txt'

        voutfile = os.path.join(gestures[currentGesture], vfilename)
        soutfile = os.path.join(gestures[currentGesture], sfilename)
        #voutfile = os.path.join(videoDir, gestures[currentGesture], vfilename)
        #soutfile = os.path.join(videoDir, gestures[currentGesture], sfilename)
        print 'output: ', voutfile

        currentIteration += 1
        extensionNumber += 1
        subprocess.call([programPath, videoFile, str(int(startPoint)), str(int(endPoint)), voutfile])

        sensorStart = startPoint - sensorPos
        sensorEnd = sensorStart + 250

        splitSensor(soutfile, int(sensorStart), int(sensorEnd))
        
        #subprocess.call([programPath, videoFile, str(splitPoints[i]), str(splitPoints[i+1]), outfile])

def onclick(event):
    global initX, initY, drag

    initX = event.xdata
    initY = event.ydata
    if toggleClick is False:
        drag = True
    if toggleAlign is True:
        drag = True
        


def onrelease(event):
    global initX, initY, splitLines, drag
    #print 'xdata=%f'%(event.xdata)

    drag = False

    return

def motion(event):
    global initX, initY, splitLines, drag

    if drag is True:

        dx =  event.xdata - initX
        dy =  event.ydata - initY

        if toggleAlign is False:

            #number of frames per video segment is 250 (50frames * 5s)
            #range to 250*numClips
            #assuming only 10 clips.. 2500
            for line in splitLines:
                x = line.get_xdata()
                y = line.get_ydata()
                line.set_data(x+dx, y+dy)
        else:
            for sensorLine in sensorLines:
                xdata = sensorLine.get_xdata()
                ydata = sensorLine.get_ydata()
                sensorLine.set_data(xdata+dx, ydata+dy)

        initX = event.xdata
        initY = event.ydata
        fig.canvas.draw()

def press(event):
    global cid, toggleClick, toggleAlign
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
            #cid = fig.canvas.mpl_connect('button_press_event', onclick)
            print 'point selection mode on'
            toggleClick = False
        else:
            #fig.canvas.mpl_disconnect(cid)
            print 'navigation mode on'
            toggleClick = True
            toggleAlign = False
    if event.key == 'a':
        if toggleAlign:
            toggleAlign = False
            toggleClick = True
        else:
            print 'aligning second graph'
            toggleAlign = True
            toggleClick = False

if len(sys.argv) != 4:
    print 'Usage: ' + sys.argv[0] + ' magnitudesFile sensorFile videoFile'
    exit()

graphFile = sys.argv[1] 
sensorFile = sys.argv[2]  
videoFile = sys.argv[3] 
videoFile = os.path.realpath(videoFile)

gestures = ('thumb','index','middle','ring','fist','point','call','gun','flex','adduct','thumb','index','middle','ring','fist','point','call','gun','flex','adduct')
numGestPerformed = 5

toggleClick = True
toggleAlign = False
drag = False

splitPoints = []
splitLines = []

data = pylab.loadtxt(graphFile)
sensorData = pylab.loadtxt(sensorFile)
#print sensorData

fig = plt.figure()
cid = fig.canvas.mpl_connect('button_press_event', onclick)
rid = fig.canvas.mpl_connect('button_release_event', onrelease)
pid = fig.canvas.mpl_connect('key_press_event', press)
mid = fig.canvas.mpl_connect('motion_notify_event', motion)

ax1 = fig.add_subplot(111)

ax1.plot(data)

offsetFrames = 24.0
sensorData = resampleUniform(sensorData, SAMPLING_FR+(20*(offsetFrames/21350.0)))
#sensorData = scipy.signal.resample(sensorData, len(sensorData)*1.097)

#print sensorData
sensorData = np.array(sensorData)


sl0, = ax1.plot(sensorData[...,1])
sl1, = ax1.plot(sensorData[...,2])
sl2, = ax1.plot(sensorData[...,3])
sl3, = ax1.plot(sensorData[...,4])
sl4, = ax1.plot(sensorData[...,5])

sensorLines = []
sensorLines.append(sl0) 
sensorLines.append(sl1) 
sensorLines.append(sl2) 
sensorLines.append(sl3) 
sensorLines.append(sl4) 

numLines = len(gestures)*numGestPerformed*250+250
for i in range(0,numLines,250):
    ln, = plt.plot([i, i], [300, -50], color='k', linestyle='-', linewidth=1)
    splitLines.append(ln)
#splitPoints.append(int(round(initX)))

plt.show()

