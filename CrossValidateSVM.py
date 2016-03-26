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

def cross_validate(gestures, originalPath):

	parentPath = os.getcwd()

	#os.chdir(trainingDir)

	features = []
	
	for i in os.listdir(os.getcwd()):
		if i in gestures:
			#print i
			os.chdir(parentPath + "/" + i)
			for dataFile in os.listdir(os.getcwd()):
				#print dataFile
				realpath = os.path.realpath(dataFile)
				#print realpath
				startfeature = time.time()
				result = extract.readFeatures(realpath)
				endfeature = time.time()
				featuretime = endfeature - startfeature
				features.append(result)

	features_scaled = (preprocessing.scale(features)).tolist()
	#print np.round(features_scaled, 2)
	#print np.round(features, 1)
	os.chdir(parentPath)

	predictions = []
	cum_rate = 0.0

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

		# iterate through parameters

		C_values = [1, 2, 8, 32, 128, 512, 2048, 8192]
		gamma_values = [0.001,0.01,0.05,0.1,0.3,0.5,0.7]

		#C_values = [2]
		#gamma_values = [0.5]

		best_C = 0
		best_G = 0
		best_percentage = 0

		#clf = svm.SVC(C=2.0,gamma=0.5)

		C_range = np.logspace(-2, 10, num=13, base=2)
		gamma_range = np.logspace(-5, 1, num=7, base=10)
		param_grid = dict(gamma=gamma_range, C=C_range)
		cv = StratifiedShuffleSplit(trainingLabels, n_iter=3, test_size=0.31, random_state=42)
		grid = GridSearchCV(svm.SVC(), param_grid=param_grid, cv=cv)
		grid.fit(trainingSet, trainingLabels)
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
		clfoutput = clf.fit(trainingSet, trainingLabels)
		result = clf.predict(testingSet)
		#end = time.time()
		#print end-start + featuretime
		predictions.append(result.tolist())
		
		num_correct = 0
		for j,k in zip(result,testingLabels):
			if j == k:
				num_correct += 1


		percentage = (float(num_correct) * 100.0) / float(len(gestures))
		#print 'percentage: ' , percentage
		best_percentage = percentage

#		 for params in itertools.product(C_values, gamma_values):
#
#			 clf = svm.SVC(C=params[0],gamma=params[1])
#			 clfoutput = clf.fit(trainingSet, trainingLabels)
## classify
#			 result = clf.predict(testingSet)
#			 predictions.append(result.tolist())
#			 
#			 num_correct = 0
#			 for j,k in zip(result,testingLabels):
#				 if j == k:
#					 num_correct += 1
#
#
#			 percentage = (float(num_correct) * 100.0) / float(len(gestures))
#			 if percentage >= best_percentage:
#				 best_percentage = percentage
#				 best_C = params[0]
#				 best_G = params[1]
#
			#print params
			#print percentage

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

	rate = cum_rate / 10.0

	print np.round(rate,2), '%'
	#print np.round(rate,3)
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
	#print 'validating:', os.path.abspath(directory)
	for r in gestures:
		#print r[1]
		cv_rate, c_matrix = cross_validate(r, originalWorkingPath)
		cv_rates.append(cv_rate)
		c_matrices.append(c_matrix)
		#print(np.round(cv_rate,2))
	os.chdir(originalWorkingPath)

	#return cv_rates, c_matrices
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
