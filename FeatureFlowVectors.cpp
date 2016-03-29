#include <opencv2/core/core.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/videoio.hpp>
#include <opencv2/video/tracking.hpp>

#include <iostream>

using namespace cv;
using namespace std;

//#define VIEW

void sampleOptFlowMap(const Mat& flow, Mat& cflowmap, int step)
{
    for(int y = step/3; y < cflowmap.rows - step/3; y += step)
        for(int x = step/3; x < cflowmap.cols - step/3; x += step)
        {
            const Point2f& f = flow.at<Point2f>(y, x);
			float fx = f.x;
			float fy = f.y;
			fx *= 30.0;
			fy *= 30.0;
			char ux = (int)fx;
			char uy = (int)fy;
			cout << ux << uy;
			//if( (int)fx < -80 ){
			//	cout << (int)fx << ',' ;//<< (int)fy << ',';
			//	cout << (int)ux << ',' ;//<< (int)fy << ',';
			//}
        }
}
static void drawOptFlowMap(const Mat& flow, Mat& cflowmap, int step,
                    double, const Scalar& color)
{
	float scale = 10.0;
    for(int y = step/3; y < cflowmap.rows - step/3; y += step)
        for(int x = step/3; x < cflowmap.cols - step/3; x += step)
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

	UMat img;
    Mat flow, cflow, frame, prevflow;
    UMat gray, prevgray, uflow;
	//double alpha = 0.6;
	double alpha = 0.8;
	double beta = (1.0 - alpha);
	bool first = 1;
	int frameCount = 0;

    for(;;frameCount++)
    {
		//if(frameCount > 4) break;

        cap >> frame;
		if (frame.empty()) break;
		
        cvtColor(frame, gray, COLOR_BGR2GRAY);
        GaussianBlur(gray, gray, Size( 5, 5), 0, 0);

        if( !prevgray.empty() )
        {
			if(first)
				calcOpticalFlowFarneback(prevgray, gray, uflow, 0.5, 3, 15, 4, 5, 1.2, 0);
			else
				calcOpticalFlowFarneback(prevgray, gray, uflow, 0.5, 2, 15, 3, 5, 1.2, OPTFLOW_USE_INITIAL_FLOW );


			//calcOpticalFlowFarneback(prevgray, gray, uflow, 0.5, 3, 15, 3, 5, 1.2, 0);
            cvtColor(prevgray, cflow, COLOR_GRAY2BGR);
            uflow.copyTo(flow);
			//thresholdFlowMatrix(flow, 1.5);
			GaussianBlur(flow, flow, Size( 15, 15), 0, 0);

            //drawOptFlowMap(flow, cflow, 16, 1.5, Scalar(0, 255, 0));
			
			// In order to average the frames
			if(!first){
				addWeighted(prevflow, alpha, flow, beta, 0.0, flow);
			}
			prevflow = flow.clone();
			first = 0;
			
            //drawOptFlowMap(flow, cflow, 16, 1.5, Scalar(0, 255, 0));
#ifdef VIEW
            drawOptFlowMap(flow, cflow, 20, 1.5, Scalar(0, 255, 0));
			imshow("flow", cflow);
#else
            sampleOptFlowMap(flow, cflow, 20);
#endif
			

        }
#ifdef VIEW
        if(waitKey(1) == 'q') break;
#endif
        std::swap(prevgray, gray);
    }
			
    return 0;
}

