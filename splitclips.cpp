#include <opencv2/core/core.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/videoio.hpp>
#include <opencv2/video/tracking.hpp>

#include <iostream>

using namespace cv;
using namespace std;

static void drawOptFlowMap(const Mat& flow, Mat& cflowmap, int step,
                    double, const Scalar& color)
{
	float scale = 10.0;
    for(int y = 0; y < cflowmap.rows; y += step)
        for(int x = 0; x < cflowmap.cols; x += step)
        {
            const Point2f& fxy = flow.at<Point2f>(y, x);
			int fx, fy;
			fx = cvRound(fxy.x*scale);
			fy = cvRound(fxy.y*scale);
			
			// red represents horizontal movement left
			// blue represents horizontal movement right

			int b = 0;
			int r = 0;
			if(fx < 0) r = fx*-1;
			else b = fx;

			Scalar col( b*20, 0, r*20);
            line(cflowmap, Point(x,y), Point(x+fx, y+fy), col, 2);
            //arrowedLine(cflowmap, Point(x,y), Point(cvRound(x+(fx*scale)), cvRound(y+(fy*scale))), col, 2);
            circle(cflowmap, Point(x,y), 1, color, 1);
        }
}

void thresholdFlowMatrix(Mat& flow, float threshold){
    for(int y = 0; y < flow.rows; y ++)
        for(int x = 0; x < flow.cols; x ++){
            Point2f& f = flow.at<Point2f>(y, x);
			if(sqrt(f.x*f.x + f.y*f.y) < threshold){
				f.x = 0.0;
				f.y = 0.0;
			}
		}
}

void absdiffRegions(const UMat& prev, const UMat& curr, UMat& dst){
	
}

double sumSqMag(Mat& flow){
	double mag = 0.0;
    for(int y = 0; y < flow.rows; y ++)
        for(int x = 0; x < flow.cols; x ++){
            Point2f& f = flow.at<Point2f>(y, x);
			//mag += sqrt(f.x*f.x + f.y*f.y);
			mag += (f.x*f.x + f.y*f.y);
		}
	return mag/1000.0;
}

void calcFlowMag(Mat& flow, Mat& result){
    for(int y = 0; y < flow.rows; y ++)
        for(int x = 0; x < flow.cols; x ++){
            Point2f& f = flow.at<Point2f>(y, x);
			result.at<float>(y,x) = sqrt(f.x*f.x + f.y*f.y);
		}
}

int main(int argc, char** argv)
{
    VideoCapture cap(argv[1]);
    if( !cap.isOpened() )
        return -1;

	double fps = cap.get(CV_CAP_PROP_FPS);
	double x_res = cap.get(CV_CAP_PROP_FRAME_WIDTH);
	double y_res = cap.get(CV_CAP_PROP_FRAME_HEIGHT);

	//cout << "fps : " << fps << endl;
	//cout << "res : " << x_res << "," << y_res << endl;


	Mat acc_flow_magnitudes;
	Mat curr_flow_magnitude;

    Mat flow, cflow, frame, prevflow;
    UMat gray, prevgray, uflow;
	UMat diffgray;
	UMat cum_diff;
    namedWindow("flow", 1);
	Rect cropRectangle(125,90,455,360);
	//double alpha = 0.6;
	double alpha = 0.9;
	double beta = (1.0 - alpha);
	bool first = 1;
	int frameCount = 0;

    for(;;frameCount++)
    {
        cap >> frame;
		if (frame.empty()) break;

        //frame = frame(cropRectangle);
        cvtColor(frame, gray, COLOR_BGR2GRAY);
        GaussianBlur(gray, gray, Size( 7, 7), 0, 0);

        if( !prevgray.empty() )
        {
			calcOpticalFlowFarneback(prevgray, gray, uflow, 0.5, 3, 15, 3, 5, 1.2, 0);
            cvtColor(prevgray, cflow, COLOR_GRAY2BGR);
            uflow.copyTo(flow);
			//thresholdFlowMatrix(flow, 1.5);

			if(!first){
				// Average the frames
				addWeighted(prevflow, alpha, flow, beta, 0.0, flow);
					
			}
			prevflow = flow.clone();

            drawOptFlowMap(flow, cflow, 16, 1.5, Scalar(0, 255, 0));
			
            imshow("flow", cflow);
			first = 0;

			double sum = sumSqMag(flow);
			cout << sum << endl;

        }
        //if(waitKey(30) == 'q')
        if(waitKey(1) == 'q')
            break;
        std::swap(prevgray, gray);
    }

	while(waitKey() != 'q'){}
			
    return 0;
}

