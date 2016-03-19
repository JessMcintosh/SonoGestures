import glob
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
    originalPath = os.path.dirname(sys.argv[0])
    os.getcwd()
    os.chdir(directory)
    print 'generating features for dir:', directory

    programPath = os.path.join(originalPath,"build", "OpenSonoGestures")
    featuresDir = os.path.join(directory, "features/")

    if not os.path.exists(featuresDir):
        os.mkdir(featuresDir)
    for i in os.listdir(os.getcwd()):
        if i in gesturesAll:
            gestureDir = os.path.join(featuresDir, i)
            if not os.path.exists(gestureDir):
                os.mkdir(gestureDir)
            print i
            os.chdir(directory + "/" + i)
            #for dataFile in os.listdir(os.getcwd()):
            for dataFile in glob.glob(os.path.join(os.getcwd(),'*.avi')):
                realpath = os.path.realpath(dataFile)
                result = extract.extract(realpath, programPath)
                basename =os.path.splitext((os.path.basename(dataFile)))[0] + ".txt"
                outfile = os.path.join(gestureDir, basename)
                print outfile
                try:
                    os.remove(outfile)
                except OSError:
                    pass
                f = open(outfile, 'w')
                f.write(result)
                f.close()
                
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

    #for i in range (2,4):
    #dirs = []
    #dirs.append("/home/nappy/Drive/SonicGesturesData/08-03-2016/dpa/")
    #dirs.append("/home/nappy/Drive/SonicGesturesData/08-03-2016/lpa/")
    #dirs.append("/home/nappy/Drive/SonicGesturesData/08-03-2016/tda/")
    #dirs.append("/home/nappy/Drive/SonicGesturesData/08-03-2016/tpa/")
    #dirs.append("/home/nappy/Drive/SonicGesturesData/08-03-2016/tpp/")
    dir = sys.argv[1]

    generate_features(os.path.abspath(dir))



