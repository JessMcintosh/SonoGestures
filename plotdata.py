import matplotlib.pyplot as plt
import numpy as np
import pylab

def onclick(event):
    print 'button=%d, x=%d, y=%d, xdata=%f, ydata=%f'%(
        event.button, event.x, event.y, event.xdata, event.ydata)
    circ = plt.Circle((event.xdata, event.ydata), radius=10, color='g')
    ax1.add_patch(circ)
    plt.show()


data = pylab.loadtxt("graphdata.txt")

fig = plt.figure()
cid = fig.canvas.mpl_connect('button_press_event', onclick)

ax1 = fig.add_subplot(111)

ax1.plot(data)
plt.show()

