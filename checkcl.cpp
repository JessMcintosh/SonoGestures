#include <iostream>
#include <fstream>
#include <string>
#include <iterator>
#include <opencv2/opencv.hpp>
#include <opencv2/core/ocl.hpp>

using namespace std;

int  main ()
{
        cv::ocl::setUseOpenCL(true);
        if  (!cv::ocl::haveOpenCL()){
        	cout  <<  "OpenCL is not available" <<  endl ;
		}
		else
		{ 
			cout << "OpenCL available" << endl;
			cout << cv::ocl::useOpenCL();
		}
}
