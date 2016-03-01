#!/bin/bash

#./OpenSonoGestures ~/Dropbox/Asier_Jess/SonicGestures/experiments/test25Feb/3\ -\ Longitudinal\ Proximal\ Anterior/Segment_trim.mp4


#./OpenSonoGestures ~/Dropbox/Asier_Jess/SonicGestures/experiments/test25Feb/3\ -\ Longitudinal\ Proximal\ Anterior/index/index0.mp4

for file in ~/Dropbox/Asier_Jess/SonicGestures/experiments/test25Feb/3\ -\ Longitudinal\ Proximal\ Anterior/index/*;  do
	echo $file
	./OpenSonoGestures "$file"
done

