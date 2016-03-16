import serial
import math
import time
import datetime
import sys
import getopt
import os
import subprocess
import extract
import numpy as np
import itertools
from sklearn import preprocessing
from sklearn.metrics import confusion_matrix
from sklearn import svm
from sklearn.cross_validation import StratifiedShuffleSplit
from sklearn.grid_search import GridSearchCV
#from svmutil import *
from time import sleep

gesturesAll = ('thumb','index','middle','ring','fist','point','call','gun','flex','adduct')

#gesturesFingers = ('Thumb', 'Index', 'Middle', 'Ring', 'Pinky')
#gesturesWrist	 = ('Ext', 'Flex', 'UDev', 'RDev', 'Pronate', 'Supinate')

#gestures = [gesturesAll, gesturesFingers, gesturesWrist]
gestures = [gesturesAll]

#trainingDirAll = 'TrainingData'
#trainingDirEMG = 'TrainingDataEMG'
#trainingDirFSR = 'TrainingDataFSR'

#trainingDirs = [trainingDirAll, trainingDirEMG, trainingDirFSR]

def generate_features(directory):
    originalPath = os.getcwd()
    clipsDir = os.path.join(directory, 'clips/')
    os.chdir(clipsDir)
    print 'generating features for dir:', clipsDir

    programPath = os.path.join(originalPath, "OpenSonoGestures")
    featuresDir = os.path.join(directory, "features/");

    if not os.path.exists(featuresDir):
        os.mkdir(featuresDir)
    for i in os.listdir(os.getcwd()):
        if i in gesturesAll:
            if not os.path.exists(os.path.join(featuresDir, i)):
                os.mkdir(os.path.join(featuresDir, i))
            print i
            os.chdir(clipsDir + "/" + i)
            for dataFile in os.listdir(os.getcwd()):
                realpath = os.path.realpath(dataFile)
                result = extract.extract(realpath, programPath)
                basename = os.path.splitext(dataFile)[0]
                outfile = os.path.join(featuresDir, i, basename+".txt")
                print outfile
                try:
                    os.remove(outfile)
                except OSError:
                    pass
                f = open(outfile, 'w')
                f.write(result)
                f.close()
                
                #features.append(result)

    #features_scaled = (preprocessing.scale(features)).tolist()
    os.chdir(originalPath)

if __name__ == '__main__':

    #cv_rate, c_matrix = cross_validate(gesturesAll, 'TrainingData')
    #print np.round(cv_rate,2), '%' 
    #print c_matrix

    #for r in itertools.product(gestures, trainingDirs):
    #	 #print r
    #	 cv_rate, c_matrix = cross_validate(r[0], r[1])
    #	 print np.round(cv_rate,2), '%' 
    #	 #print c_matrix
    
    all_c_matrices = []
    sum_c_matrices = []

    #for i in range (2,4):
    dirs = []
    dirs.append("/home/nappy/Drive/SonicGesturesData/08-03-2016/dpa/")
    dirs.append("/home/nappy/Drive/SonicGesturesData/08-03-2016/lpa/")
    dirs.append("/home/nappy/Drive/SonicGesturesData/08-03-2016/tda/")
    dirs.append("/home/nappy/Drive/SonicGesturesData/08-03-2016/tpa/")
    dirs.append("/home/nappy/Drive/SonicGesturesData/08-03-2016/tpp/")

    generate_features(dirs[0])
