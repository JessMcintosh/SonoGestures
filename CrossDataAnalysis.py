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
from GraphConfusionMatrix import plot_confusion_matrix
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

def cross_validate(trainingDir, testingDir):

	parentPath = os.getcwd()

	os.chdir(trainingDir)
	trainingFeatures = []
        trainingLabels = []
	
	for i in os.listdir(os.getcwd()):
		if i in gesturesAll:
			#print i
			os.chdir(trainingDir + "/" + i)
                        for dataFile in os.listdir(os.getcwd()):
				#print dataFile
				realpath = os.path.realpath(dataFile)
				#print realpath
				startfeature = time.time()
				result = extract.readFeatures(realpath)
				endfeature = time.time()
				featuretime = endfeature - startfeature
				trainingFeatures.append(result)
                                trainingLabels.append(i)

	trainingFeatures = (preprocessing.scale(trainingFeatures)).tolist()

	os.chdir(testingDir)
	testingFeatures = []
	testingLabels = []

	for i in os.listdir(os.getcwd()):
		if i in gesturesAll:
			#print i
			os.chdir(testingDir + "/" + i)
			for dataFile in os.listdir(os.getcwd()):
				#print dataFile
				realpath = os.path.realpath(dataFile)
				#print realpath
				startfeature = time.time()
				result = extract.readFeatures(realpath)
				endfeature = time.time()
				featuretime = endfeature - startfeature
				testingFeatures.append(result)
                                testingLabels.append(i)

	testingFeatures = (preprocessing.scale(testingFeatures)).tolist()
	os.chdir(parentPath)

	#print np.round(features_scaled, 2)
	#print np.round(features, 1)

	predictions = []

        #for feature_vector in features_scaled:
        #        if count%10 == 0:
        #                currentGesture += 1
        #        if count%10 == i:
        #                testingSet.append(feature_vector)
        #                testingLabels.append(currentGesture)
        #        else:
        #                trainingSet.append(feature_vector)
        #                trainingLabels.append(currentGesture)
        #        count += 1

        best_percentage = 0

        C_range = np.logspace(-2, 10, num=13, base=2)
        gamma_range = np.logspace(-5, 1, num=7, base=10)
        param_grid = dict(gamma=gamma_range, C=C_range)
        cv = StratifiedShuffleSplit(trainingLabels, n_iter=3, test_size=0.31, random_state=42)
        grid = GridSearchCV(svm.SVC(), param_grid=param_grid, cv=cv)
        grid.fit(trainingFeatures, trainingLabels)
        #C_range = np.logspace(-1, 1, num=2, base=2)
        #gamma_range = np.logspace(-1, 1, num=2, base=10)
        #param_grid = dict(gamma=gamma_range, C=C_range)
        #cv = StratifiedShuffleSplit(trainingLabels, n_iter=1, test_size=0.11, random_state=42)
        #grid = GridSearchCV(svm.SVC(), param_grid=param_grid, cv=cv)
        #grid.fit(trainingSet, trainingLabels)

        best_C = grid.best_params_['C']
        best_G = grid.best_params_['gamma']
        #print("The best parameters are %s with a score of %0.2f"
        #			   % (grid.best_params_, grid.best_score_))


        #start = time.time()
        clf = svm.SVC(C=best_C,gamma=best_G)
        clfoutput = clf.fit(trainingFeatures, trainingLabels)
        result = clf.predict(testingFeatures)
        #end = time.time()
        #print end-start + featuretime
        predictions.append(result.tolist())
        
        num_correct = 0
        for j,k in zip(result,testingLabels):
                if j == k:
                        num_correct += 1

        percentage = (float(num_correct) * 100.0) / 100.0
	print np.round(percentage,2), '%'

	c_matrix = confusion_matrix(testingLabels, result) 
	print c_matrix
        plot_confusion_matrix(c_matrix,"confusionmatrix")

	return percentage, c_matrix

def validate_participant(dir1, dir2):
	cv_rates = []
	c_matrices = []

	print 'validating:', dir1, dir2
        cv_rate, c_matrix = cross_validate(dir1, dir2)
        cv_rates.append(cv_rate)
        c_matrices.append(c_matrix)
        print(np.round(cv_rate,2))

	return cv_rates, c_matrices

if __name__ == '__main__':

	cv_rates, c_matrices = validate_participant(os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2]))
