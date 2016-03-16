import time
import datetime
import sys
from sys import argv
import getopt
import os
import subprocess
import csv
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy import stats
from numpy import genfromtxt

#from sklearn import svm, datasets

def conv(s):
    try:
        s=int(s)
    except ValueError:
        pass
    return s

def convert(s):
    newarray = [conv(i) for i in s]
    return newarray

def plot_confusion_matrix(cm, file, title='Confusion matrix', cmap=plt.cm.Blues):

    norm_conf = []
    #for i in cm:
    #    a = 0
    #    tmp_arr = []
    #    a = sum(i, 0)
    #    for j in i:
    #        tmp_arr.append((float(j)/float(a))*100)
    #    norm_conf.append(tmp_arr)


    fig = plt.figure()
    plt.clf()
    ax = fig.add_subplot(111)
    ax.set_aspect(1)
    #res = ax.imshow(np.array(norm_conf), cmap=plt.cm.Blues, 
    #                interpolation='nearest')
    res = ax.imshow(np.array(cm), cmap=plt.cm.Blues, 
                    interpolation='nearest')

    width = len(cm)
    height = len(cm[0])

    for x in xrange(width):
        for y in xrange(height):
            if cm[x][y] > 0:
                if cm[x][y] > 4:
                    ax.annotate(str(cm[x][y]), xy=(y, x), 
                        horizontalalignment='center',
                        verticalalignment='center', color = 'white',
                        fontsize = 11)
                elif cm[x][y] < 2:
                    ax.annotate(str(cm[x][y]), xy=(y, x), 
                        horizontalalignment='center',
                        verticalalignment='center', color = 'black',
                        fontsize = 11)
                else:
                    ax.annotate(str(cm[x][y]), xy=(y, x), 
                        horizontalalignment='center',
                        verticalalignment='center', color = 'gray',
                        fontsize = 11)
                        
    res.set_clim(vmin=0, vmax=5)

    cb = fig.colorbar(res)
    alphabet = '012345678910'
    #gesture_nums = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]

    gesture_nums = ('thumb','index','middle','ring','fist','point','call','gun','flex','adduct')
    #gesture_nums = ['Pro.', 'Fist', 'Point', 'Ring', 'Flex', 'Index', 'Sup.', 'Thumb', 'Spread', 'Middle', 'Adb.', 'Add.', 'Ext.', 'Pinky', 'Palm']

    #gesture_nums = ['Ring', 'Index', 'Thumb', 'Middle', 'Pinky']

    #gesture_nums = ['Pronate', 'Flex', 'Supinate', 'Abduction', 'Adduction', 'Extension']

    #plt.tight_layout()
    plt.xlabel('True')
    plt.ylabel('Predicted')
    
    plt.xticks(range(width), gesture_nums, rotation=45)
    plt.yticks(range(height), gesture_nums)
    ax.grid(True, alpha=0.2)
    plt.savefig(file + '.pdf', format='pdf', bbox_inches='tight')

    #plt.imshow(cm, interpolation='nearest', cmap=cmap)
    #plt.title(title)
    #plt.colorbar()
    ##tick_marks = np.arange(len(iris.target_names))
    ##plt.xticks(tick_marks, iris.target_names, rotation=45)
    ##plt.yticks(tick_marks, iris.target_names)
    #plt.show()
    #plt.savefig(file + '.png', format='png')

def plotgraph(file):
	data = genfromtxt(file, delimiter=',')
	data = np.transpose(data)
	errors = stats.sem(data)
	mean = np.mean(data, axis=1)
	print mean
	print errors

	fig = plt.figure(figsize=(6,6))
	ax = fig.add_subplot(1, 1, 1)

	gestures = ['Finger', 'Wrist', 'All']
	x = np.arange(1,4,1)	
	EMG=  (mean[4], mean[7], mean[1])
	FSR=  (mean[5], mean[8], mean[2]) 
	Both= (mean[3], mean[6], mean[0])
	EMG_err =  (errors[4], errors[7], errors[1])
	FSR_err =  (errors[5], errors[8], errors[2]) 
	Both_err = (errors[3], errors[6], errors[0])

	#ls = 'dotted'
	B = plt.errorbar(x-0.03, 	Both, 	yerr=Both_err, color='red', ls='-', fmt='o', label='Both')
	E = plt.errorbar(x, 		EMG, 	yerr=EMG_err, color='blue', ls='-', fmt='o', label='EMG')
	F = plt.errorbar(x+0.03, 	FSR, 	yerr=FSR_err, color='green', ls='-', fmt='o', label='FSR')
	#plt.legend()
	box = ax.get_position()
	#ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

# Put a legend to the right of the current axis
	#ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
	ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05),
			          ncol=3, fancybox=True, shadow=True,
                                  prop={'size':11})
	#plt.legend(bbox_to_anchor=(1.05, 1), loc=2)
	#plt.plot(x-0.05, Both, 	color='red')
	#plt.plot(x, 	EMG, 	color='blue')
	#plt.plot(x+0.05, FSR, 	color='green')
	ax.set_xlim([0.5,3.5])
	ax.xaxis.set_tick_params(width=12)
	plt.ylabel('10-fold cross validation %', fontsize=12)
	plt.xlabel('Gesture set', fontsize=12)
	#plt.xticks(np.arange(0, 4, 1.0))
	plt.xticks(np.arange(1, 4, 1.0), gestures)
        matplotlib.rcParams.update({'font.size': 11})
	#plt.yticks(np.arange(84, 100, 2))
        ax.set_axis_bgcolor((0.90, 1.00, 0.90))
	#plt.show()
	plt.savefig(file + '.pdf', format='pdf', bbox_inches='tight')

if __name__ == '__main__':
    plotgraph(argv[1])
