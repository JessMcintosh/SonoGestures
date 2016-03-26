#!/usr/bin/python

import pylab
import serial
import time
import datetime
import sys
import getopt
import os
import subprocess
import json
import pyexcel as pe
from time import sleep
from itertools import izip
from pyexcel_ods import save_data
#from CrossValidateSVM import validate_participant
from CrossValidateNN import validate_participant
from collections import OrderedDict

features = ['features', 'FeaturesFlowMag']
locations = ['dpa', 'lpa', 'tda', 'tpa']
#locations = ['dpa', 'lpa', 'tda', 'tpa', 'tpp']
participants = ['Asier', 'Jess']

cv_rates_all = []
c_matrices_all = []

featureSet = sys.argv[2]

if len(sys.argv) > 3:
    participants = [sys.argv[3]]

# set up spreadsheet
data = OrderedDict() 

data_path = os.path.abspath(sys.argv[1])

for p in participants:
    cv_rates = []
    c_matrices = []
    cv_rates.append(p)

    for loc in locations:
        print p, loc
        path = os.path.join(data_path, p, loc, featureSet)
        cv_rate, c_matrix = validate_participant(path)
        cv_rates.append(cv_rate)
        c_matrices.append(c_matrix)

    cv_rates_all.append(cv_rates)
    c_matrices_all.append(c_matrices)

cv_averages = []
for i in range(len(locations)+1):
    if i == 0:
        continue
    cv_averages.append(0.0)
for rates in cv_rates_all:
    for i in range(len(locations)+1):
        if i == 0:
            continue
        cv_averages[i-1] += rates[i]
for i in range(len(locations)+1):
    if i == 0:
        continue
    cv_averages[i-1] = cv_averages[i-1] / len(c_matrices_all)

cv_averages.insert(0, 'avg')
locations.insert(0, 'participant')

cv_rates_all.insert(0, locations)
cv_rates_all.append(cv_averages)

data.update({featureSet: cv_rates_all})
#data.update({"Sheet 1": [cv_rates]})
save_data("results.ods", data)
sheet = pe.get_book(file_name="results.ods")
print sheet

exit(0);
