import pylab
import sys
import os

#uniformly resamples the matrix data using data[][0] as the timestamps
# the returned data still contains the timestamp (uniform now) in data[][0]
def resampleUniform(data, samplingPeriod):
    rows = len(data[0])
    columns = len(data)
    
    r = []
        
    currentTime = data[0][0]
    currentIndex = 0
       
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
        currentTime += samplingPeriod
        
    return r


sensorFile = raw_input('data file ')
resampleRate = int(raw_input('sampling rate '))
sensorFile = os.path.realpath(sensorFile)

data = pylab.loadtxt(sensorFile)
data = resampleUniform(data, resampleRate)
pylab.savetxt(sensorFile + ".txt", data,'%d')
