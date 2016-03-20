#include <opencv2/core/core.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/videoio.hpp>
#include <opencv2/video/tracking.hpp>

#include <iostream>
#include <vector>

using namespace cv;
using namespace std;

#define FEATURES_SPACE 32

#define INDEX(a,b,c, sizeY) ((sizeY*3* a) + 3*b + c)

static void calcFeatures(const Mat& image, const int separation, vector<double>& features){
	const cv::Size size = image.size();
	const int x_res = size.width;
	const int y_res = size.height;
	const int nx_features = x_res / FEATURES_SPACE;
	const int ny_features = y_res / FEATURES_SPACE;


	Mat roi = image(cv::Rect(0, 0, separation, separation));
	CvMoments moments;
	for (int ix = 0; ix < nx_features; ++ix){
		for (int iy = 0; iy < ny_features; ++iy){
			const cv::Rect roiBounds(ix * separation, iy * separation, separation, separation);
			roi = image(roiBounds);

			double F0, F1, F2;
			IplImage iRoi = roi;
			cvMoments(&iRoi, &moments);

			const int findex = INDEX(ix, iy, 0, ny_features);
			features[findex + 0] = cvGetSpatialMoment(&moments, 0, 0);
			features[findex + 1] = 2 * cvGetCentralMoment(&moments, 1, 1);
			features[findex + 2] = cvGetCentralMoment(&moments, 2, 0) - cvGetCentralMoment(&moments, 0, 2);
		}
	}
}

static void drawFeatures(Mat& image, const vector<double>& features){
	const cv::Size size = image.size();
	const int x_res = size.width;
	const int y_res = size.height;
	const int nx_features = x_res / FEATURES_SPACE;
	const int ny_features = y_res / FEATURES_SPACE;

	const Scalar blue(128, 128, 128);
	for (int ix = 0; ix < nx_features; ++ix){
		for (int iy = 0; iy < ny_features; ++iy){
			const Point p(ix * FEATURES_SPACE + (FEATURES_SPACE / 2), iy * FEATURES_SPACE + (FEATURES_SPACE / 2));

			const int findex = INDEX(ix, iy, 0, ny_features);
			const double N = FEATURES_SPACE * FEATURES_SPACE * 256;
			const double f0 = features[findex + 0] / N * 10;
			const double f1 = features[findex + 1] / N * 2;
			const double f2 = features[findex + 2] / N * 2;

			line(image, p, Point(p.x + f1, p.y - f2), blue, 2);
			circle(image, p, f0, blue, 3);
		}
	}
}

int main(int argc, char** argv){
	std::string fileName = "";
	bool showImage = true;

	if (argc == 1){ //no arguments 
		fileName = "C:/Users/am14010/Google Drive/SonicGesturesData/18-03-2016/Asier/lpa/index/index0.avi";
		//fileName = "C:/Users/am14010/Google Drive/SonicGesturesData/tmp/testOrientation.mp4";
		showImage = true;
	}else if (argc == 2){
		fileName = argv[1];
		showImage = false;
	}
	else if (argc == 3){
		fileName = argv[1];
		showImage = true;
	}

	VideoCapture cap( fileName.c_str() );
    if( !cap.isOpened() )
        return -1;

	const int fps = cap.get(CV_CAP_PROP_FPS);
	const int x_res = cap.get(CV_CAP_PROP_FRAME_WIDTH);
	const int y_res = cap.get(CV_CAP_PROP_FRAME_HEIGHT);

	const int nx_features = x_res / FEATURES_SPACE;
	const int ny_features = y_res / FEATURES_SPACE;

	std::vector<double> features(nx_features * ny_features * 3);

	Mat frame, gray;
  	
	for (int frameCount = 0; ;frameCount++){
        cap >> frame;
		if (frame.empty()) break;
		
        cvtColor(frame, gray, COLOR_BGR2GRAY);
        GaussianBlur(gray, gray, Size(5, 5), 0, 0);

		//calc the features
		calcFeatures(gray, FEATURES_SPACE, features);

		if (!showImage){
			//output into the standard input
			const int l = features.size();
			for (int i = 0; i < l; ++i){
				cout << features[i] << " ";
			}
			cout << endl;
		}
		else{
			//draw them
			drawFeatures(gray, features);
			imshow("raw image with blur", gray);
		}
		
		if (showImage && waitKey(50) == 'q') break;
    
	}

    return 0;
}

