#include <algorithm>
#include <cmath>
#include <opencv/cv.h>
#include <opencv/cv.hpp>
#include <opencv/highgui.h>
#include <stdio.h>

bool isSign(std::vector<cv::Point>& contour)
{
	double area = cv::contourArea(contour);
	if (area < 500) return false;
	cv::Rect rect = cv::boundingRect(contour);
	if (std::abs(1 - (float)rect.width / rect.height) > 0.1) return false;
	return true;
}
static size_t total_blocker_width = 0;
bool couldBeBlock(std::vector<cv::Point>& contour)
{
	double area = cv::contourArea(contour);
	if (area < 300) return false;
	cv::Rect rect = cv::boundingRect(contour);
	if (std::abs(1 - ((float)rect.width / 1.8) / rect.height) > 0.2) return false;
	total_blocker_width += rect.width;
	return true;
}
int main(int argc, char** argv)
{
	cv::VideoCapture cap(0);
	cap.set(CV_CAP_PROP_BUFFERSIZE, 1);

	while(true) {

		getchar();

		if(!cap.isOpened())
			return 1;

		total_blocker_width = 0;

		cv::Mat frame;
		cap >> frame;
		cap >> frame;
		cap >> frame;
		cap >> frame;
		cap >> frame;

		cv::Point2f src_center(frame.cols/2.0F, frame.rows/2.0F);
		cv::Mat rot_mat = cv::getRotationMatrix2D(src_center, 180, 1.0);
		cv::Mat img;
		cv::warpAffine(frame, img, rot_mat, frame.size());

		cv::imwrite("last.jpg", img);

		cv::cvtColor(img, img, CV_BGR2HSV);

		cv::Mat mask1(img.size(), img.type());
		cv::Mat mask2(img.size(), img.type());
		cv::inRange(img, cv::Scalar(0, 30, 30), cv::Scalar(15, 255, 255), mask1);
		cv::inRange(img, cv::Scalar(165, 30, 30), cv::Scalar(180, 255, 255), mask2);
		cv::bitwise_or(mask1, mask2, img);

		std::vector<std::vector<cv::Point>> contours;
		cv::findContours(img, contours, CV_RETR_TREE, CV_CHAIN_APPROX_NONE);
		bool sign_detected = false;
		for (auto contour : contours) {
			if (!sign_detected)
				sign_detected = isSign(contour);
			
			couldBeBlock(contour);

			if (total_blocker_width > 250)
				break;
		}

		if (total_blocker_width > 250)
			puts("rb");
		else if (sign_detected)
			puts("stop");
		else
			puts("nothing");

	}
	return 0;
}
