#include "pch.h"
#include <opencv2/opencv.hpp>
#include "ColorDetection.h"



using namespace cv;

extern "C"
{
    void DetectColors(unsigned char* input, int width, int height, int channels, float* lowerHSV, float* upperHSV, int* numContours)
    {
        Mat image(height, width, CV_8UC3, input);
        Mat hsvImage;

        cvtColor(image, hsvImage, COLOR_BGR2HSV);

        Scalar lowerBound(lowerHSV[0], lowerHSV[1], lowerHSV[2]);
        Scalar upperBound(upperHSV[0], upperHSV[1], upperHSV[2]);

        Mat binaryImage;
        inRange(hsvImage, lowerBound, upperBound, binaryImage);

        std::vector<std::vector<Point>> contours;
        findContours(binaryImage, contours, RETR_EXTERNAL, CHAIN_APPROX_SIMPLE);

        *numContours = static_cast<int>(contours.size());
    }
}