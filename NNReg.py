#!/usr/bin/python

import sys
import os
import pylab
import numpy as np
import math
from sklearn import linear_model
from sklearn.neural_network import MLPClassifier
from sklearn.cross_validation import StratifiedShuffleSplit
from sklearn.grid_search import GridSearchCV
from sklearn.multiclass import OneVsOneClassifier
from sklearn.multiclass import OneVsRestClassifier

FEATURES_NAME = "FeatureFramesMoments"

#GESTURES = ["call","fist","gun","index","middle","point","ring","thumb","adduct","flex"]
GESTURES = ["index","middle","ring","thumb","call","fist","gun"]
N_GESTURES = 10
N_FINGERS = 5

#P = N A + b it returns A and b
def regression(N, P):
    assert len(N) == len(P)
    
    clf = linear_model.Ridge (alpha = .1)
    clf.fit (N, P)
    #r = {"A":clf.coef_, "b":clf.intercept_}
    return clf.coef_, clf.intercept_

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


if len(sys.argv) != 2:
    print 'Usage: ' + sys.argv[0] + ' path'
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

#cross validation
for i in range(0, 1):
#for i in range(0, N_GESTURES):
    #skip i
    training = range(0, N_GESTURES)
    training.remove( i )
    sample = [i]
    
    #for n in range (0, N_FINGERS):
    for n in range (0, 1):
        print "Regression " + str(i) + "/" + str(N_GESTURES) + " for finger " + str(n)
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
        
        A, b = regression(trainingN, trainingP)
        errors[n] += calcNRMS(A, b, sampleN, sampleP)

print "---------- " 
for n in range (0, N_FINGERS):
    print "NRMS for finger " + str(n) + " " + ("%.2f" % (errors[n]/N_GESTURES*100))
