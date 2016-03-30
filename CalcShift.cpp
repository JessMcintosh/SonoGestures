#include <opencv2/core/core.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/videoio.hpp>
#include <opencv2/video/tracking.hpp>

#include <iostream>

using namespace cv;
using namespace std;

#define VIEW

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
Point2f getTranslation(const Mat& flow, int offset)
{
	float scale = 0.4;
	float count = 0;
	float t_x = 0, t_y = 0;
    for(int y = offset; y < flow.rows - offset; y ++)
        for(int x = offset; x < flow.cols - offset; x ++)
        {
            const Point2f& f = flow.at<Point2f>(y, x);
			t_x += f.x;
			t_y += f.y;
			count += 1.0;
        }
	t_x /= count*scale;
	t_y /= count*scale;
	return Point2f(t_x, t_y);
}
static void drawOptFlowMap(const Mat& flow, Mat& cflowmap, int step,
                    double scale, const Scalar& color)
{
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
            line(cflowmap, Point(x,y), Point(x+fx, y+fy), col, 1);
            //arrowedLine(cflowmap, Point(x,y), Point(cvRound(x+(fx*scale)), cvRound(y+(fy*scale))), col, 2);
            circle(cflowmap, Point(x,y), 1, color, 1);
        }
}

Mat translateImg(Mat &img, int offsetx, int offsety){
	Mat trans_mat = (Mat_<double>(2,3) << 1, 0, offsetx, 0, 1, offsety);
	warpAffine(img,img,trans_mat,img.size());
	return trans_mat;
}

int main(int argc, char** argv)
{
    VideoCapture cap1(argv[1]);
    if( !cap1.isOpened() )
        return -1;
    VideoCapture cap2(argv[2]);
    if( !cap2.isOpened() )
        return -1;

    namedWindow("flow", 1);
    namedWindow("gray1", 1);
    namedWindow("gray2", 1);
    namedWindow("gray2_translated", 1);

	UMat img;
    Mat flow, cflow, frame, prevflow, shifted;
    UMat gray1, uflow, gray2;
	//double alpha = 0.6;
	double alpha = 0.8;
	double beta = (1.0 - alpha);

	cap1 >> frame;
	cap1 >> frame;
	cap1 >> frame;
	cvtColor(frame, gray1, COLOR_BGR2GRAY);
	imshow("gray1", gray1);
	GaussianBlur(gray1, gray1, Size( 15, 15), 0, 0);

	cap2 >> frame;
	cap2 >> frame;
	cap2 >> frame;
	cvtColor(frame, gray2, COLOR_BGR2GRAY);
	imshow("gray2", gray2);
	GaussianBlur(gray2, gray2, Size( 15, 15), 0, 0);

	calcOpticalFlowFarneback(gray1, gray2, uflow, 0.5, 5, 50, 6, 7, 1.5, 0);
	uflow.copyTo(flow);
	GaussianBlur(flow, flow, Size( 15, 15), 0, 0);

	Point2f T = getTranslation(flow, 10);
	translateImg(frame, -T.x, -T.y);

	prevflow = flow.clone();

	int frameCount = 0;

    for(;frameCount < 0;frameCount++)
    {
		cap1 >> frame;
		cap1 >> frame;
		cap1 >> frame;
		cvtColor(frame, gray1, COLOR_BGR2GRAY);
		GaussianBlur(gray1, gray1, Size( 5, 5), 0, 0);
		
		cap2 >> frame;
		cap2 >> frame;
		cap2 >> frame;
		cvtColor(frame, gray2, COLOR_BGR2GRAY);
		GaussianBlur(gray2, gray2, Size( 5, 5), 0, 0);

		calcOpticalFlowFarneback(gray1, gray2, uflow, 0.5, 4, 15, 4, 5, 1.2, 0);
		uflow.copyTo(flow);
		GaussianBlur(flow, flow, Size( 15, 15), 0, 0);

		addWeighted(prevflow, alpha, flow, beta, 0.0, flow);
		prevflow = flow.clone();
	}
			
#ifdef VIEW
	cvtColor(gray1, cflow, COLOR_GRAY2BGR);
	drawOptFlowMap(flow, cflow, 10, 1.5, Scalar(0, 255, 0));
	imshow("gray1", gray1);
	imshow("gray2", gray2);
	imshow("gray2_translated", frame);
	imshow("flow", cflow);
	waitKey();
#endif
			
    return 0;
}

