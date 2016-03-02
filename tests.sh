#!/bin/bash

#./OpenSonoGestures ~/Dropbox/Asier_Jess/SonicGestures/experiments/test25Feb/3\ -\ Longitudinal\ Proximal\ Anterior/Segment_trim.mp4

#./OpenSonoGestures ~/Dropbox/Asier_Jess/SonicGestures/experiments/test25Feb/3\ -\ Longitudinal\ Proximal\ Anterior/index/index0.mp4

videodir="~/Dropbox/Asier_Jess/SonicGestures/experiments/test25Feb/3 - Longitudinal Proximal Anterior/"

echo $videodir

for file in `ls -a $videodir`; do
	echo $file
done

exit 

for file in ~/Dropbox/Asier_Jess/SonicGestures/experiments/test25Feb/3\ -\ Longitudinal\ Proximal\ Anterior/thumb/*;  do
	#echo $file
	printf "0 "
	./OpenSonoGestures "$file"
done

for file in ~/Dropbox/Asier_Jess/SonicGestures/experiments/test25Feb/3\ -\ Longitudinal\ Proximal\ Anterior/index/*;  do
	#echo $file
	printf "1 "
	./OpenSonoGestures "$file"
done

for file in ~/Dropbox/Asier_Jess/SonicGestures/experiments/test25Feb/3\ -\ Longitudinal\ Proximal\ Anterior/middle/*;  do
	#echo $file
	printf "2 "
	./OpenSonoGestures "$file"
done

for file in ~/Dropbox/Asier_Jess/SonicGestures/experiments/test25Feb/3\ -\ Longitudinal\ Proximal\ Anterior/ring/*;  do
	#echo $file
	printf "3 "
	./OpenSonoGestures "$file"
done

for file in ~/Dropbox/Asier_Jess/SonicGestures/experiments/test25Feb/3\ -\ Longitudinal\ Proximal\ Anterior/pinky/*;  do
	#echo $file
	printf "4 "
	./OpenSonoGestures "$file"
done

for file in ~/Dropbox/Asier_Jess/SonicGestures/experiments/test25Feb/3\ -\ Longitudinal\ Proximal\ Anterior/fist/*;  do
	#echo $file
	printf "5 "
	./OpenSonoGestures "$file"
done
