from subprocess import call
import os
import sys

PATH = "/home/nappy/Drive/SonicGesturesData/18-03-2016"
EXEC = "NNReg.py"

program = os.path.join( os.path.dirname(sys.argv[0]) ,EXEC) 

for participant in os.listdir(PATH):
    pDir = os.path.join(PATH, participant)
    if (os.path.isdir( pDir)):
        for location in os.listdir(pDir):
            lDir = os.path.join(pDir, location, "FeatureFramesMoments")
            if (os.path.isdir( lDir)):
                print participant, " ", location
                call(["python", program, lDir])