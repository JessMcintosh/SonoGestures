/*
	Program used to remap videos in order to correct shifts

	The videos to be process are passed as arguments to the program
	If no argument is passed then the programm reads the standard input until an empty line is detected and treats each line as a file to process

	to mark the frames use the left button.
	right button to skip to the next frame
	medium button to return to the previous frame

	once that all the videos have been marked, the remapping will take place
*/

#include <opencv2/core/core.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/videoio.hpp>

#include <iostream>
#include <vector>
#include <string>


using namespace cv;
using namespace std;

#define MAX_POINTS 4
static bool markingPoints = false;
static int currentPoint = 0;
static int buttonPressed = 0;
static int xPressed = 0, yPressed = 0;
typedef struct { Point2f p[MAX_POINTS]; } PointPack;

static string addPostFixToFilename(const string& s, const string& add){
	const int lastindex = s.find_last_of(".");
	if (lastindex != -1){
		return s.substr(0, lastindex) + add + s.substr(lastindex);
	}
	return s;
}

static string getFileName(const string& s){
	const int lastindex = std::max<int>(s.find_last_of("/"), s.find_last_of("\\"));
	if (lastindex != -1){
		return s.substr(lastindex+1);
	}
	return s;
}

void CallBackFunc(int event, int x, int y, int flags, void* userdata){
	if (markingPoints){
		if (event == EVENT_LBUTTONDOWN || event == EVENT_RBUTTONDOWN || event == EVENT_MBUTTONDOWN){
			xPressed = x;
			yPressed = y;
			buttonPressed = event;
			markingPoints = false;
		}
	}
}

int main(int argc, char** argv){

	vector<string> files;
	
	if (argc == 1){
		//read the files to be remapped
		while (true){
			string mystr;
			getline(cin, mystr);
			if (mystr.empty()){
				break;
			}
			files.push_back(mystr);
		}
	}
	else{
		for (int i = 1; i < argc; ++i){
			files.push_back(argv[i]);
		}
	}

	const int nVideos = files.size();
	vector<PointPack> points(nVideos);
	cout << "Processing " << nVideos << " videos" << endl;

	

	Mat frame;
	int currentVideo = 0;
	bool copyPoints = true;

	for (int currentVideo = 0; currentVideo < nVideos;){
		const string fileName = files[currentVideo];
		const string baseName = getFileName(fileName);
		PointPack& pointPack = points[currentVideo];

		VideoCapture cap(fileName.c_str());
		if (!cap.isOpened()){
			cerr << "Error opening file " << fileName;
			continue;
		}
		
		//get first frame
		cap >> frame;
		if (frame.empty()) {
			cerr << "Error reading file " << fileName;
			continue;
		}

		//copy points from the previous frame or init them if it is the first frame
		if (copyPoints){
			if (currentVideo == 0){
				for (int i = 0; i < MAX_POINTS; ++i){
					pointPack.p[i].x = 0;
					pointPack.p[i].y = 0;
				}
			}
			else{
				const PointPack& prevPoint = points[currentVideo - 1];
				for (int i = 0; i < MAX_POINTS; ++i){
					pointPack.p[i] = prevPoint.p[i];
				}
			}
		}

		std::ostringstream o;
		o << currentVideo << "/" << nVideos << " " << baseName;

		copyPoints = true;
		for (currentPoint = 0; currentPoint < MAX_POINTS;){
			//draw the points
			for (int i = 0; i < MAX_POINTS; ++i){
				
				cv::putText(frame, o.str(), Point(20, 20), FONT_HERSHEY_PLAIN, 1, Scalar::all(255));

				circle(frame, pointPack.p[i], 1, Scalar::all(255), 6);
				circle(frame, pointPack.p[i], 1, Scalar::all(128), 4);
				circle(frame, pointPack.p[i], 1, Scalar::all(0), 2);
			}
			imshow("currentFrame", frame);
			setMouseCallback("currentFrame", CallBackFunc, NULL);

			markingPoints = true;
			while (markingPoints){ //Sorry about this lame waiting
				waitKey(5);
			}

			if (buttonPressed == EVENT_LBUTTONDOWN){//normal button --> mark the point
				pointPack.p[currentPoint].x = xPressed;
				pointPack.p[currentPoint].y = yPressed;
				currentPoint++;
				if (currentPoint >= MAX_POINTS){
					currentVideo++;
					break;
				}
			}
			else if (buttonPressed == EVENT_RBUTTONDOWN){//right button <-- next video
				currentVideo++;
				break;
			}
			else if (buttonPressed == EVENT_MBUTTONDOWN){//middle button <-- previous video
				if (currentVideo > 0){
					currentVideo--;
					copyPoints = false;
					break;
				}
			}
		}
	}

	if (nVideos > 0){
		//exporting the remapped videos
		const PointPack& firstPointPack = points[0];

		for (int currentVideo = 0; currentVideo < nVideos; ++currentVideo){ //we convert also the first video to keep errors consistent
			const string fileName = files[currentVideo];
			const string outputName = addPostFixToFilename(fileName,"_remap");
			PointPack& pointPack = points[currentVideo];

			//create the transformation matrix
			

#if MAX_POINTS == 3
			Mat lambda(2, 3, CV_32FC1);
			lambda = getAffineTransform(pointPack.p, firstPointPack.p);
#elif MAX_POINTS == 4
			Mat lambda( 3, 3, CV_32FC1 );
			lambda = getPerspectiveTransform(pointPack.p, firstPointPack.p);	
#else
#error MAX_POINTS should be either 3 or 4
#endif


			VideoCapture cap( fileName );
			cout << "remaping " << fileName << endl;

			const int fps = cap.get(CV_CAP_PROP_FPS);
			const int x_res = cap.get(CV_CAP_PROP_FRAME_WIDTH);
			const int y_res = cap.get(CV_CAP_PROP_FRAME_HEIGHT);

			VideoWriter outputVideo;
			//'D','I','V','X'
			//'X', '2', '6', '4'
			outputVideo.open(outputName, CV_FOURCC('X', '2', '6', '4'), fps, Size(x_res, y_res), true);
			while (true){
				cap >> frame;
				if (frame.empty()) break;

				//remap the frame
#if MAX_POINTS == 3
				warpAffine(frame, frame, lambda, frame.size());
#elif MAX_POINTS == 4
				warpPerspective(frame, frame, lambda, frame.size());
#endif

				outputVideo << frame;
			}

		}

	}

    return 0;
}

