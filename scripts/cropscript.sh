#!/bin/bash 

ffmpeg -i tda/Segment_0001.mp4 -an -filter:v "crop=534:345:84:94" tda/cropped.mp4
ffmpeg -i tpp/Segment_0001.mp4 -an -filter:v "crop=534:345:84:94" tpp/cropped.mp4
ffmpeg -i dpa/Segment_0001.mp4 -an -filter:v "crop=438:345:130:94" dpa/cropped.mp4
ffmpeg -i lpa/Segment_0001.mp4 -an -filter:v "crop=438:345:130:94" lpa/cropped.mp4
ffmpeg -i tpa/Segment_0001.mp4 -an -filter:v "crop=438:345:130:94" tpa/cropped.mp4
