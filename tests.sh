#!/bin/bash

#./OpenSonoGestures ~/Dropbox/Asier_Jess/SonicGestures/experiments/test25Feb/3\ -\ Longitudinal\ Proximal\ Anterior/Segment_trim.mp4


#./OpenSonoGestures ~/Dropbox/Asier_Jess/SonicGestures/experiments/test25Feb/3\ -\ Longitudinal\ Proximal\ Anterior/index/index0.mp4

for file in ~/Dropbox/Asier_Jess/SonicGestures/experiments/test25Feb/3\ -\ Longitudinal\ Proximal\ Anterior/thumb/*;  do
	echo $file
	./OpenSonoGestures "$file"
done


for file in ~/Dropbox/Asier_Jess/SonicGestures/experiments/test25Feb/3\ -\ Longitudinal\ Proximal\ Anterior/index/*;  do
	echo $file
	./OpenSonoGestures "$file"
done

for file in ~/Dropbox/Asier_Jess/SonicGestures/experiments/test25Feb/3\ -\ Longitudinal\ Proximal\ Anterior/middle/*;  do
	echo $file
	./OpenSonoGestures "$file"
done

for file in ~/Dropbox/Asier_Jess/SonicGestures/experiments/test25Feb/3\ -\ Longitudinal\ Proximal\ Anterior/ring/*;  do
	echo $file
	./OpenSonoGestures "$file"
done

for file in ~/Dropbox/Asier_Jess/SonicGestures/experiments/test25Feb/3\ -\ Longitudinal\ Proximal\ Anterior/pinky/*;  do
	echo $file
	./OpenSonoGestures "$file"
done

for file in ~/Dropbox/Asier_Jess/SonicGestures/experiments/test25Feb/3\ -\ Longitudinal\ Proximal\ Anterior/fist/*;  do
	echo $file
	./OpenSonoGestures "$file"
done
