#!/usr/bin/python

import sys
import os
import pylab
import numpy as np
import math
from sklearn import linear_model
import matplotlib.pyplot as plt

#GESTURES = ["call","fist","gun","index","middle","point","ring","thumb","adduct","flex"]
GESTURES = ["index","middle","ring","thumb","call","fist","gun"]
N_GESTURES = 10
N_FINGERS = 5

#P = N A + b it returns A and b
def regression(N, P):
    assert len(N) == len(P)
    
    clf = linear_model.Ridge (alpha = .1)
    clf.fit (N, P)
    r = {"A":clf.coef_, "b":clf.intercept_}
    return r

def dotProduct(A,B):
    r = 0
    for i in range(0, len(A)):
        r += A[i] * B[i]
    return r
    
#in theory NA + b = P
def calcNRMS(A,b, N,P):
    rowsN = len(N);
    rowsA = len(A);
    colsN = len(N[0]);
    sizeP = len(P);
    
    assert sizeP == rowsN  and colsN == rowsA
    nrms = 0
    minV = sys.float_info.max
    maxV = -sys.float_info.max
    for i in range(0, colsN):
        realValue = P[i]
        predictedValue = dotProduct(N[i], A) + b
        diff = realValue - predictedValue
        minV = min(minV, realValue)
        maxV = max(maxV, realValue)
        nrms += diff*diff
    
    return math.sqrt(nrms/colsN) / (maxV - minV)


def loadFile(path):
    return pylab.loadtxt(path)


def median(data):
    data = sorted(data)
    n = len(data)
    if n%2 == 1:
        return data[n//2]
    else:
        i = n//2
        return (data[i - 1] + data[i])/2
    
# applies a median filter on the vector with window size a
def medianFilter(data, a):
    n = len(data)
    for i in range(0,n-a): #TODO sorry about the borders and the not centered window
        data[i] = median( data[i:i+a] );
    return;

# applies a low pass filter as v[t] = s*alpha + v[t-1]*(1-alpha)
def lowPassFilter(data, alpha):   
    beta = (1 - alpha)
    n = len(data)
    for i in range(1,n):
        data[i] = data[i]*alpha + data[i-1]*beta
    return;

verbose = True
if len(sys.argv) == 2:
    verbose = False
elif len(sys.argv) == 3:
    verbose = True
else:
    print 'Usage: ' + sys.argv[0] + ' path [verbose]'
    exit()
    
featuresPath =  os.path.realpath(sys.argv[1])
fingersPath = os.path.dirname( os.path.realpath(featuresPath))

#load data features(gesture)(trial), fingers(gesture)(trial)
features = {}
fingers = {}
for ig in GESTURES:
    features[ig] = []
    fingers[ig] = []
    for inu in range(0,N_GESTURES):
        featurePath = os.path.join(featuresPath, ig, ig+str(inu) + ".txt")
        fingerPath = os.path.join(fingersPath, ig, ig+str(inu) + ".txt")
        features[ig].append( loadFile(featurePath) )
        fingers[ig].append( loadFile(fingerPath).T )
        
#generate the sampling, training
errors = np.zeros( N_FINGERS );

#filter the glove data

for ig in GESTURES:
    for n in range(0,N_GESTURES):
        for f in range(0,N_FINGERS):
            currentList = fingers[ig][n][f]
            #copyList = list( currentList )
            #listRange = range(0, len(currentList))
            medianFilter(currentList, 15)
            #lowPassFilter(fingers[ig][n][f], 0.1)
            #plt.plot(listRange, copyList, 'r--', listRange, currentList, 'bs')
            #plt.show()
            
#cross validation
for i in range(0, N_GESTURES):
    #skip i
    training = range(0, N_GESTURES)
    training.remove( i )
    sample = [i]
    
    for n in range (0, N_FINGERS):
        #if verbose:
            #print "Regression " + str(i) + "/" + str(N_GESTURES) + " for finger " + str(n)
            
        #create N and P
        trainingN = []
        trainingP = []
        sampleN = []
        sampleP = []
        
        for ig in GESTURES:
            for inu in training:
                trainingN.extend( features[ig][inu] )
                trainingP.extend( fingers[ig][inu][n] )
            for inu in sample:
                sampleN.extend( features[ig][inu] ) 
                sampleP.extend( fingers[ig][inu][n] )
        
        result = regression(trainingN, trainingP)
        errors[n] += calcNRMS(result["A"], result["b"], sampleN, sampleP)

if verbose:
    print "---------- "
average = 0
for n in range (0, N_FINGERS):
    percentage = (errors[n]/N_GESTURES*100)
    average += percentage
    if verbose:
        print "NRMS for finger " + str(n) + " " + ("%.2f" % percentage)
average /= N_FINGERS
print str(average)