#include <opencv2/core/core.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/videoio.hpp>
#include <opencv2/video/tracking.hpp>

#include <iostream>

using namespace cv;
using namespace std;

//int main(int argc, char* argv[])
//{
//    cv::VideoCapture cap(argv[1]);
//    if (!cap.isOpened())
//    {
//        std::cout << "!!! Failed to open file: " << argv[1] << std::endl;
//        return -1;
//    }
//
//    cv::Mat frame;
//	cv::Mat of_frame;
//    for(;;)
//    {
//
//        if (!cap.read(frame))             
//            break;
//
//        cv::imshow("window", frame);
//
//		cv::calcOpticalFlowFarneback(frame, of_frame, InputOutputArray flow, double pyr_scale, int levels, int winsize, int iterations, int poly_n, double poly_sigma, int flags)
//
//        char key = cvWaitKey(10);
//        if (key == 27) // ESC
//            break;
//    }
//
//    return 0;
//}

static void drawOptFlowMap(const Mat& flow, Mat& cflowmap, int step,
                    double, const Scalar& color)
{
	float scale = 10.0;
    for(int y = 0; y < cflowmap.rows; y += step)
        for(int x = 0; x < cflowmap.cols; x += step)
        {
            const Point2f& fxy = flow.at<Point2f>(y, x);
			int fx, fy;
			//if(sqrt(fxy.x*fxy.x + fxy.y*fxy.y) < 0.5){
			//	fx = 0; fy = 0;
			//}
			//else{
			//	fx = (int)fxy.x*scale;
			//	fy = (int)fxy.y*scale;
			//}
			fx = cvRound(fxy.x*scale);
			fy = cvRound(fxy.y*scale);
            //line(cflowmap, Point(x,y), Point(cvRound(x+(fx*scale)), cvRound(y+(fy*scale))),
			
			// red represents horizontal movement left
			// blue represents horizontal movement right

			int b = 0;
			int r = 0;
			if(fx < 0) r = fx*-1;
			else b = fx;

			Scalar col( b*20, 0, r*20);
            line(cflowmap, Point(x,y), Point(cvRound(x+fx), cvRound(y+fy)), col, 2);
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

int main(int argc, char** argv)
{
    VideoCapture cap(argv[1]);
    if( !cap.isOpened() )
        return -1;

    Mat flow, cflow, frame, prevflow;
    UMat gray, prevgray, uflow;
	UMat diffgray;
    namedWindow("flow", 1);
	Rect cropRectangle(125,90,455,360);
	double alpha = 0.5;
	double beta = (1.0 - alpha);
	bool first = 1;

    for(;;)
    {
        cap >> frame;
        frame = frame(cropRectangle);
        cvtColor(frame, gray, COLOR_BGR2GRAY);
        GaussianBlur(gray, gray, Size( 7, 7), 0, 0);

        if( !prevgray.empty() )
        {
			//calcOpticalFlowPyrLK();
			//createOptFlow_DualTVL1();
			calcOpticalFlowFarneback(prevgray, gray, uflow, 0.5, 3, 15, 3, 5, 1.2, 0);
            cvtColor(prevgray, cflow, COLOR_GRAY2BGR);
            uflow.copyTo(flow);
			if(!first)
			addWeighted(prevflow, alpha, flow, beta, 0.0, flow);
			prevflow = flow.clone();
			//thresholdFlowMatrix(flow, 1.5);
			//GaussianBlur(flow, flow, Size( 31, 31), 0, 0);
            //drawOptFlowMap(flow, cflow, 8, 1.5, Scalar(0, 255, 0));
            drawOptFlowMap(flow, cflow, 16, 1.5, Scalar(0, 255, 0));
            imshow("flow", cflow);
			first = 0;

			absdiff(prevgray, gray, diffgray);
			imshow("diff", diffgray);
        }
        //if(waitKey(30) == 'q')
        if(waitKey(1) == 'q')
            break;
        std::swap(prevgray, gray);
    }
    return 0;
}

