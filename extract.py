from struct import *
import time
import re
import datetime
import sys
from sys import argv
import getopt
import os
import subprocess
import csv
import numpy as np

def readFeatures(file):
	features = []
	f = open(file)
	result = f.read()
	for token in result.split():
		try:
			features.append(float(token))
		except ValueError:
			print "non float value detected"

	#features = re.findall("\d+\.\d+", result)

	return features

def getSumVector(file):
	features =	readBinaryFile(file)
	#features = [abs(x) for x in features]
	featureAbs = []
	for x in features:
		z = [abs(y) for y in x]
		featureAbs.append(z)
	floats = [float(sum(x)) for x in zip(*featureAbs)]
	return floats

def getSumVectorHalf1(file):
	features =	readBinaryFile(file)
	featurehalf = features[:126]
	#features = [abs(x) for x in features]
	floats = [float(sum(x)) for x in zip(*featurehalf)]
	return floats

def getSumVectorHalf2(file):
	features =	readBinaryFile(file)
	featurehalf = features[126:]
	#features = [abs(x) for x in features]
	floats = [float(sum(x)) for x in zip(*featurehalf)]
	return floats

def readBinaryFile(file):
#for line in f
#remember 374 bytes per frame
	features = []
	f = open(file)
	result = f.read()
	#print result
	frameLength = len(result)/249
	bytearray = list(unpack(str(len(result))+'b', result))
	#bytearray = abs(bytearray)

	return [ bytearray[n:n+frameLength] for n,i in enumerate(bytearray) if n%(frameLength)==0 ] 

def extract(file, programPath):
	return subprocess.check_output([programPath, file])

def extract_features(data):
	feature_vector = []

	for i in data:
		#numbering starts: feature 0
		#feature_vector.append(np.mean(i))	#0
		feature_vector.append(np.amax(i))	#1
		#feature_vector.append(np.amin(i))	#2
		feature_vector.append(rms(i))		#3
		#feature_vector.append(np.sum(i))	#4
		feature_vector.append(np.std(i))	#5
		#feature_vector.append(np.var(i))	#6

	#feature_vector.append(np.correlate(i))

	return feature_vector

if __name__ == '__main__':
	#extract(argv[1])
	#r = readBinaryFile(argv[1])
	getSumVector(argv[1])
