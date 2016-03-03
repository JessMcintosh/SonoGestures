#include <opencv2/core/core.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/videoio.hpp>
#include <opencv2/video/tracking.hpp>

#include <iostream>

using namespace cv;
using namespace std;

int main(int argc, char** argv)
{
	int startFrame = atoi(argv[2]);
	int endFrame = atoi(argv[3]);

	cout << "start frame: " << startFrame;
	cout << "end frame: " << endFrame;

	char* fileName = argv[4];

    VideoCapture cap(argv[1]);
    if( !cap.isOpened() )
        return -1;

	double fps = cap.get(CV_CAP_PROP_FPS);
	double x_res = cap.get(CV_CAP_PROP_FRAME_WIDTH);
	double y_res = cap.get(CV_CAP_PROP_FRAME_HEIGHT);

	//cout << "fps : " << fps << endl;
	//cout << "res : " << x_res << "," << y_res << endl;

	Rect cropRectangle(125,90,455,360);

	VideoWriter outputVideo;

	vector<Mat> split;
	int ex = static_cast<int>(cap.get(CV_CAP_PROP_FOURCC));

	//outputVideo.open(fileName, CV_FOURCC('F','M','P','4'), fps, Size(x_res,y_res), true);
	outputVideo.open(fileName, CV_FOURCC('M','M','P','4'), fps, Size(x_res,y_res), true);
	Mat frame;

	int frameCount = 0;
	for(; frameCount < startFrame; frameCount++){
		cap >> frame;
	}
    for(;frameCount < endFrame; frameCount++)
    {
        cap >> frame;
		if (frame.empty()) break;
		outputVideo << frame;

        //frame = frame(cropRectangle);
        //cvtColor(frame, gray, COLOR_BGR2GRAY);
        //GaussianBlur(gray, gray, Size( 7, 7), 0, 0);

        //if(waitKey(1) == 'q')
            //break;
    }
			
    return 0;
}

