import matplotlib.pyplot as plt
import numpy as np
import pylab
import sys

def onclick(event):
    global initX, initY
    print 'button=%d, x=%d, y=%d, xdata=%f, ydata=%f'%(
        event.button, event.x, event.y, event.xdata, event.ydata)
    
    initX = event.xdata
    initY = event.ydata

def onrelease(event):
    global initX, initY
    print 'button=%d, x=%d, y=%d, xdata=%f, ydata=%f'%(
        event.button, event.x, event.y, event.xdata, event.ydata)

    if initX == event.xdata and initY == event.ydata:
        #circ = plt.Circle((event.xdata, event.ydata), radius=2, color='g')
        #ax1.add_patch(circ)
        ln = plt.plot([event.xdata, event.xdata], [1000, -1000], color='k', linestyle='-', linewidth=2)
        fig.canvas.draw()
        splitPoints.append(int(round(initX)))
        splitLines.append(ln)

def press(event):
    global cid, toggleClick
    #print('press', event.key)
    sys.stdout.flush()

    if event.key == 'w':
        print splitPoints
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

toggleClick = False

splitPoints = []
splitLines = []

data = pylab.loadtxt("graphdata.txt")

fig = plt.figure()
cid = fig.canvas.mpl_connect('button_press_event', onclick)
rid = fig.canvas.mpl_connect('button_release_event', onrelease)
pid = fig.canvas.mpl_connect('key_press_event', press)

ax1 = fig.add_subplot(111)

ax1.plot(data)
plt.show()

