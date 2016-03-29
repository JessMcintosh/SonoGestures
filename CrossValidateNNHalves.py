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
from sklearn.neural_network import MLPClassifier
from sklearn.cross_validation import StratifiedShuffleSplit
from sklearn.grid_search import GridSearchCV
from sklearn.multiclass import OneVsOneClassifier
from sklearn.multiclass import OneVsRestClassifier
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

def cross_validate(gestures, originalPath):

	parentPath = os.getcwd()

	#os.chdir(trainingDir)

	features = []

        print 'Reading features...'
	
	for i in os.listdir(os.getcwd()):
		if i in gestures:
			#print i, 'flex'
			os.chdir(parentPath + "/" + i)
			for dataFile in os.listdir(os.getcwd()):
				#print dataFile
				realpath = os.path.realpath(dataFile)
                                firsthalf = extract.getSumVectorHalf1(realpath)
				features.append(firsthalf)
			#print i, 'extend'
			os.chdir(parentPath + "/" + i)
			for dataFile in os.listdir(os.getcwd()):
				#print dataFile
				realpath = os.path.realpath(dataFile)
                                secondhalf = extract.getSumVectorHalf2(realpath)
				features.append(secondhalf)

        print 'Features loaded.'
	features_scaled = (preprocessing.scale(features)).tolist()
	#print np.round(features_scaled, 2)
	#print np.round(features, 1)
	os.chdir(parentPath)

	predictions = []
	cum_rate = 0.0

        print 'Classifying...'

# loop through 10 times
	for i in range(10):
		#print 'fold' , i 
# select subset of features for the fold
		count = 0
		trainingSet		= []
		testingSet		= []
		trainingLabels	= []
		testingLabels	= []
		currentGesture = -1

		#for i in range(len(features)):
		#	 print features[i]
		#print '\n\n\n\n'
		#for feature_vector in features:
		#	 print feature_vector 

		for feature_vector in features_scaled:
			if count%10 == 0:
				currentGesture += 1
			if count%10 == i:
				testingSet.append(feature_vector)
				testingLabels.append(currentGesture)
			else:
				trainingSet.append(feature_vector)
				trainingLabels.append(currentGesture)
			count += 1

# train the data on the new subset

		#start = time.time()
		#clf = MLPClassifier(algorithm='l-bfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
		#clf.fit(trainingSet, trainingLabels)
		#clf.predict(testingSet)

		#clf = OneVsOneClassifier(MLPClassifier(algorithm='l-bfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1))                
		clf = OneVsRestClassifier(MLPClassifier(algorithm='l-bfgs', alpha=1e-1, hidden_layer_sizes=(15, ), random_state=1))                
		#clf = OneVsRestClassifier(MLPClassifier(algorithm='l-bfgs', alpha=1e-4, hidden_layer_sizes=(3, ), random_state=1))                

		trainingSet = np.array(trainingSet)
		trainingLabels = np.array(trainingLabels)
		testingSet = np.array(testingSet)
		
		clf.fit(trainingSet, trainingLabels)
		result = clf.predict(testingSet)
		#print result

		#result = OneVsOneClassifier(MLPClassifier(algorithm='l-bfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)).fit(trainingSet, trainingLabels).predict(testingSet)

		#print result

		#clfoutput = clf.fit(trainingSet, trainingLabels)
		#result = clf.predict(testingSet)
		#end = time.time()
		#print end-start + featuretime
		predictions.append(result.tolist())
		
		num_correct = 0
		for j,k in zip(result,testingLabels):
			if j == k:
				num_correct += 1


		percentage = (float(num_correct) * 100.0) / float(len(gestures*2))
		#print 'percentage: ' , percentage
		best_percentage = percentage


		cum_rate += best_percentage
		#print np.round(percentage,2), '%'

		#print 'best percentage: ', best_percentage
		#print 'best C: ', best_C
		#print 'best G: ', best_G

		#print result



		#prob = svm_problem(trainingLabels, trainingSet)
		#param = svm_parameter('-s 0 -t 2 -c 2 -g 0.5')
		#param = svm_parameter('-s 0 -t 2 -c 2 -g 0.5')
		#m = svm_train(prob, param)
		#p_label, p_acc, p_val = svm_predict(testingLabels, testingSet, m)
		#print p_label

		#print p_acc
		#print p_val
	#print predictions
        print 'Classification complete.'

	rate = cum_rate / 10.0

	print np.round(rate,3), '%'
	linear_pred = []
	linear_true = []
	for i in predictions:
		count = 0 
		for j in i:
			linear_pred.append(j)
			linear_true.append(count)
			count += 1
	
	#print linear_pred
	#print linear_true

	c_matrix = confusion_matrix(linear_true, linear_pred) 
	#print c_matrix
        #plot_confusion_matrix(c_matrix,"confusionmatrix")

	return rate, c_matrix

def validate_participant(directory):
	cv_rates = []
	c_matrices = []

	originalWorkingPath = os.getcwd()
	#os.chdir(os.path.join(directory, "features/"))
	os.chdir(os.path.abspath(directory))
	#print 'validating:', directory
	for r in gestures:
		#print r[1]
		cv_rate, c_matrix = cross_validate(r, originalWorkingPath)
		cv_rates.append(cv_rate)
		c_matrices.append(c_matrix)
	os.chdir(originalWorkingPath)

	return cv_rate, c_matrix

if __name__ == '__main__':

	#cv_rate, c_matrix = cross_validate(gesturesAll, 'TrainingData')
	#print np.round(cv_rate,2), '%' 
	#print c_matrix

	#for r in itertools.product(gestures, trainingDirs):
	#	 #print r
	#	 cv_rate, c_matrix = cross_validate(r[0], r[1])
	#	 print np.round(cv_rate,2), '%' 
	#	 #print c_matrix
	
	#all_c_matrices = []
	#sum_c_matrices = []

	#for i in range (2,4):
	#dirs = []
	#dirs.append("/home/nappy/Drive/SonicGesturesData/08-03-2016/dpa/")
	#dirs.append("/home/nappy/Drive/SonicGesturesData/08-03-2016/lpa/")
	#dirs.append("/home/nappy/Drive/SonicGesturesData/08-03-2016/tda/")
	#dirs.append("/home/nappy/Drive/SonicGesturesData/08-03-2016/tpa/")
	#dirs.append("/home/nappy/Drive/SonicGesturesData/08-03-2016/tpp/")

	#cv_rates, c_matrices = validate_participant(dirs[0])
	#cv_rates, c_matrices = validate_participant(dirs[1])
	#cv_rates, c_matrices = validate_participant(dirs[2])
	#cv_rates, c_matrices = validate_participant(dirs[3])
	#cv_rates, c_matrices = validate_participant(dirs[4])

	cv_rates, c_matrices = validate_participant(sys.argv[1])
	#all_c_matrices.append(c_matrices)

    


	# FOR CONFUSION MATRICES

	#first = True
	#for idx, n in enumerate(all_c_matrices):
	#	 if first: 
	#		 sum_c_matrices = n
	#		 first = False
	#	 else:
	#		 for idy, j in enumerate(sum_c_matrices):
	#			 sum_c_matrices[idy] = sum_c_matrices[idy] + all_c_matrices[idx][idy]

			#for idx, n in enumerate(zip(sum_c_matrices, i)):
			#	 print idx
			#	 print n
			#	 
			#	 n[0] = n[0] + n[1]
	#sum_c_matrices[:] = [((x * 100.0) / 120.0) for x in sum_c_matrices]
	#for x in sum_c_matrices:
	#	 for y in x:
	#		 for idx, z in enumerate(y):
	#			 if idx != len(y) - 1:
	#				 print '%d,' % z, 
	#			 else:
	#				 print '%d' % z
	#print all_c_matrices
