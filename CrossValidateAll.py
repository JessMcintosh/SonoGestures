#!/usr/bin/python

import pylab
import serial
import time
import datetime
import sys
import getopt
import os
import subprocess
from time import sleep
from itertools import izip

features = ('FeaturesAll.dat', 'FeaturesAllEMG.dat', 'FeaturesAllFSR.dat',
            'FeaturesFingers.dat', 'FeaturesFingersEMG.dat', 'FeaturesFingersFSR.dat',
            'FeaturesWrist.dat', 'FeaturesWristEMG.dat', 'FeaturesWristFSR.dat')
parentPath = os.getcwd()

for i in range (2,10):
    #print 'Test_0' + str(i) + '/Features.dat'
    dir = 'Test_0' + str(i)
    os.chdir(dir)
    print dir, 'generating feature vectors...'
    subprocess.call(['./GenerateFeatureVectors.py'])
    os.chdir(parentPath)
    for n in features:
        arg = dir + '/' + n
        print arg
        subprocess.call(['./easy.py', arg])

dir = 'Test_10'
os.chdir(dir)
print dir, 'generating feature vectors...'
subprocess.call(['./GenerateFeatureVectors.py'])
os.chdir(parentPath)
for n in features:
    arg = 'Test_10' + '/' + n
    subprocess.call(['./easy.py', arg])

dir = 'Test_11'
os.chdir(dir)
print dir, 'generating feature vectors...'
subprocess.call(['./GenerateFeatureVectors.py'])
os.chdir(parentPath)
for n in features:
    arg = 'Test_11' + '/' + n
    subprocess.call(['./easy.py', arg])

dir = 'Test_12'
os.chdir(dir)
print dir, 'generating feature vectors...'
subprocess.call(['./GenerateFeatureVectors.py'])
os.chdir(parentPath)
for n in features:
    arg = 'Test_12' + '/' + n
    subprocess.call(['./easy.py', arg])

dir = 'Test_13'
os.chdir(dir)
print dir, 'generating feature vectors...'
subprocess.call(['./GenerateFeatureVectors.py'])
os.chdir(parentPath)
for n in features:
    arg = 'Test_13' + '/' + n
    subprocess.call(['./easy.py', arg])
exit(0)

for i in os.listdir(dir_pressure):
	print i 
	for n in os.listdir(os.path.join(dir_pressure, i)):
		print n
		#result = subprocess.check_output(["paste", "-d ", os.path.join(dir_pressure, i, m), os.path.join(dir_EMG, j, n)])
		result = subprocess.check_output(["cut", "-d", " ", "-f5,6,7,8", os.path.join(dir_pressure, i, n)])
        #ts = time.time()
        #filename = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
		
		r_path = os.path.join(dir_output, i)
		if not os.path.exists(os.path.join(dir_output, i)):
			os.makedirs(r_path)

		f = open(os.path.join(r_path, n), 'w')
		f.write(result)
		f.close()

exit(0)
