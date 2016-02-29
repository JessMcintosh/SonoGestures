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


static void help()
{
    cout <<
            "\nThis program demonstrates dense optical flow algorithm by Gunnar Farneback\n"
            "Mainly the function: calcOpticalFlowFarneback()\n"
            "Call:\n"
            "./fback\n"
            "This reads from video camera 0\n" << endl;
}
static void drawOptFlowMap(const Mat& flow, Mat& cflowmap, int step,
                    double, const Scalar& color)
{
	float scale = 1.1;
    for(int y = 0; y < cflowmap.rows; y += step)
        for(int x = 0; x < cflowmap.cols; x += step)
        {
            const Point2f& fxy = flow.at<Point2f>(y, x);
			int fx, fy;
			if(sqrt(fxy.x*fxy.x + fxy.y*fxy.y) < 0.5){
				fx = 0; fy = 0;
			}
			else{
				fx = fxy.x;
				fy = fxy.y;
			}
            line(cflowmap, Point(x,y), Point(cvRound(x+(fx*scale)), cvRound(y+(fy*scale))),
                 color, 2);
            circle(cflowmap, Point(x,y), 1, color, 1);
        }
}

void blurFlowMatrix(const Mat& flow, Mat& result){
    //for(int y = 0; y < cflowmap.rows; y += step)
        //for(int x = 0; x < cflowmap.cols; x += step)

}

int main(int argc, char** argv)
{
    cv::CommandLineParser parser(argc, argv, "{help h||}");
    if (parser.has("help"))
    {
        help();
        return 0;
    }
    VideoCapture cap(argv[1]);
    help();
    if( !cap.isOpened() )
        return -1;

    Mat flow, cflow, frame;
    UMat gray, prevgray, uflow;
    namedWindow("flow", 1);

    for(;;)
    {
        cap >> frame;
        cvtColor(frame, gray, COLOR_BGR2GRAY);
        GaussianBlur(gray, gray, Size( 7, 7), 0, 0);

        if( !prevgray.empty() )
        {
			//calcOpticalFlowPyrLK();
			//createOptFlow_DualTVL1();
			calcOpticalFlowFarneback(prevgray, gray, uflow, 0.5, 3, 15, 3, 5, 1.2, 0);
            cvtColor(prevgray, cflow, COLOR_GRAY2BGR);
            uflow.copyTo(flow);
			//blurFlowMatrix(flow, flow);
			//GaussianBlur(flow, flow, Size( 31, 31), 0, 0);
            drawOptFlowMap(flow, cflow, 8, 1.5, Scalar(0, 255, 0));
            imshow("flow", cflow);
        }
        if(waitKey(30)>=0)
            break;
        std::swap(prevgray, gray);
    }
    return 0;
}

