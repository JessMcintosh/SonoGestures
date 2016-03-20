import cv2
import sys
import os
import getopt
import subprocess
import datetime
import numpy as np

outputDir = 'Data'

try:
    cap = cv2.VideoCapture(sys.argv[1])
except:
    print 'No video path given'
    exit(1)


video = cv2.VideoWriter('output.mp4')

while(cap.isOpened()):
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

