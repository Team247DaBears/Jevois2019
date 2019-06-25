#include<iostream>
#include<vector>
#include<stdio.h>
#include<opencv2/highgui/highgui.hpp>
#include<opencv2/imgproc/imgproc.hpp>
#include<opencv2/opencv.hpp>

using namespace std;
using namespace cv;
int main() 
{
Mat inimg = imread("practice7354.png");
 transpose(inimg,inimg);
  flip(inimg,inimg, 1);
  Scalar lowColor = Scalar(53, 20, 211);
  Scalar highColor = Scalar(86, 255, 255);
  Mat imghls;
  cvtColor(inimg, imghls, CV_BGR2HLS);
  Mat mask;
  inRange(imghls, lowColor, highColor, mask);

  vector<vector<Point> > contours;
  vector<Vec4i> hierarchy;

  /// Find contours
  findContours(mask, contours, hierarchy, CV_RETR_TREE, CV_CHAIN_APPROX_SIMPLE, Point(0, 0));


 int biggestIndex = -1;
 int secondIndex = -1;
 double biggestSize = 0;

 double  secondSize = 0;
 int  index = 0;
 

 if (contours.size() > 0)
 {
	 //for (auto contour = contours.begin(); contour != contours.end(); ++contour)
	 for(int i=0;i<contours.size();i++)
	 {
		 double cArea = contourArea(contours[i]);
		 if (cArea > biggestSize)
		 {
			 secondSize = biggestSize;
			 secondIndex = biggestIndex;
			 biggestSize = cArea;
			 biggestIndex = i;
		 }
		 else if (cArea > secondSize)
		 {
			 secondSize = cArea;
			 secondIndex = i;
		 }



	 }

	 RotatedRect brect1, brect2;
	 Point2f rectPoints1[4];
	 Point2f rectPoints2[4];

	 if (biggestIndex > -1)
	 {
		 brect1 = minAreaRect(contours[biggestIndex]);
		 brect1.points(rectPoints1);
	 }

	 if (secondIndex > -1)
	 {
		 brect2 = minAreaRect(contours[secondIndex]);
		 brect2.points(rectPoints2);
	 }



	 int v1 = 321; //there ought to be an easier way, but......
	 int	 v2 = 321;
	 int	 v3 = 321;
	 int	 v4 = 321;

	 int	 v1i = -1;
	 int	 v2i = -1;
	 int	 v3i = -1;
	 int	 v4i = -1;

		 //This is possibly the dumbest sort I've ever done.  But it works and I was tired.
		 //It is really a modification of some earlier code, that made sense.

	 for (int i = 0; i < 4; i++)
	 {
		 if (rectPoints1[i].y < v1)
		 {
			 v4i = v3i;
			 v3i = v2i;
			 v2i = v1i;
			 v1i = i;

			 v4 = v3;
			 v3 = v2;
			 v2 = v1;
			 v1 = rectPoints1[i].y;
		 }
		 else if (rectPoints1[i].y < v2)
		 {
			 v4i = v3i;
			 v3i = v2i;
			 v2i = i;

			 v4 = v3;
			 v3 = v2;
			 v2 = rectPoints1[i].y;
		 }

		 else if (rectPoints1[i].y < v3)
		 {
			 v4i = v3i;
			 v3i = i;

			 v4 = v3;
			 v3 = rectPoints1[i].y;
		 }

		 else if (rectPoints1[i].y < v4)
		 {
			 v4i = i;
			 v4 = rectPoints1[i].y;
		 }
	 }//end of i=0 to 3


		 Point2f point1_1 = rectPoints1[v1i];
		 Point2f point2_1 = rectPoints1[v2i];
		 Point2f point3_1 = rectPoints1[v3i];
		 Point2f point4_1 = rectPoints1[v4i];

		 /////////////Now do the second rectangle


		     v1 = 321; //there ought to be an easier way, but......
		 	 v2 = 321;
		 	 v3 = 321;
		 	 v4 = 321;

		 	 v1i = -1;
		 	 v2i = -1;
		 	 v3i = -1;
		 	 v4i = -1;

		 //This is possibly the dumbest sort I've ever done.  But it works and I was tired.
		 //It is really a modification of some earlier code, that made sense.

		 for (int i = 0; i < 4; i++)
		 {
			 if (rectPoints2[i].y < v1)
			 {
				 v4i = v3i;
				 v3i = v2i;
				 v2i = v1i;
				 v1i = i;

				 v4 = v3;
				 v3 = v2;
				 v2 = v1;
				 v1 = rectPoints2[i].y;
			 }
			 else if (rectPoints2[i].y < v2)
			 {
				 v4i = v3i;
				 v3i = v2i;
				 v2i = i;

				 v4 = v3;
				 v3 = v2;
				 v2 = rectPoints2[i].y;
			 }

			 else if (rectPoints2[i].y < v3)
			 {
				 v4i = v3i;
				 v3i = i;

				 v4 = v3;
				 v3 = rectPoints2[i].y;
			 }

			 else if (rectPoints2[i].y < v4)
			 {
				 v4i = i;
				 v4 = rectPoints2[i].y;
			 }
		 }//end of i=0 to 3


		 Point2f point1_2 = rectPoints2[v1i];
		 Point2f point2_2 = rectPoints2[v2i];
		 Point2f point3_2 = rectPoints2[v3i];
		 Point2f point4_2 = rectPoints2[v4i];


		

		 vector<Point2f> imagePoints;
		 imagePoints.push_back(point1_1);
		 imagePoints.push_back(point2_1);
		 imagePoints.push_back(point3_1);
		 imagePoints.push_back(point4_1);
		 imagePoints.push_back(point1_2);
		 imagePoints.push_back(point2_2);
		 imagePoints.push_back(point3_2);
		 imagePoints.push_back(point4_2);

		 vector<Point3f> objPoints;
		 Point3f objPoints1 = Point3f(-5.94, 0.5, 0);
		 Point3f ObjPoints2 = Point3f(-4, 0, 0);
		 Point3f ObjPoints3 = Point3f(-7.19, -4.34, 0);
		 Point3f ObjPoints4 = Point3f(-5.25, -4.84, 0);
		 Point3f ObjPoints5 = Point3f(5.94, 0.5, 0);
		 Point3f ObjPoints6 = Point3f(4, 0, 0);
		 Point3f ObjPoints7 = Point3f(7.19, -4.34,0);
		 Point3f ObjPoints8 = Point3f(5.25, -4.84, 0);

		 if (point1_1.x < point1_2.x)
		 {
			 objPoints.push_back(objPoints1);
			 objPoints.push_back(ObjPoints2);
			 objPoints.push_back(ObjPoints3);
			 objPoints.push_back(ObjPoints4);
			 objPoints.push_back(ObjPoints5);
			 objPoints.push_back(ObjPoints6);
			 objPoints.push_back(ObjPoints7);
			 objPoints.push_back(ObjPoints8);
		 }
		 else
		 {
			 objPoints.push_back(ObjPoints5);
			 objPoints.push_back(ObjPoints6);
			 objPoints.push_back(ObjPoints7);
			 objPoints.push_back(ObjPoints8);
			 objPoints.push_back(objPoints1);
			 objPoints.push_back(ObjPoints2);
			 objPoints.push_back(ObjPoints3);
			 objPoints.push_back(ObjPoints4);

		 }

		 cv::Mat distCoeffs(5, 1, cv::DataType<double>::type);
		 distCoeffs.at<double>(0) = 0;
		 distCoeffs.at<double>(1) = 0;
		 distCoeffs.at<double>(2) = 0;
		 distCoeffs.at<double>(3) = 0;
		 distCoeffs.at<double>(4) = 0;


		 cv::Mat cameraMatrix(3, 3, cv::DataType<double>::type);
		// cameraMatrix.row(0).at<double>(0) = 335;
		 cameraMatrix.at<double>(0, 0) = 335;
		 cameraMatrix.row(0).at<double>(1)= 0;
		 cameraMatrix.row(0).at<double>(2) = 120;
		 cameraMatrix.row(1).at<double>(0) = 0;
		 cameraMatrix.row(1).at<double>(1) = 335;
		 cameraMatrix.row(1).at<double>(2) = 160;
		 cameraMatrix.row(2).at<double>(0) = 0;
		 cameraMatrix.row(2).at<double>(1) = 0;
		 cameraMatrix.row(2).at<double>(2) = 1;
		 

		 cv::Mat rvec(3, 1, cv::DataType<double>::type);
		 cv::Mat tvec(3, 1, cv::DataType<double>::type);



		 cv::solvePnP(objPoints, imagePoints, cameraMatrix, distCoeffs, rvec, tvec);


		 double transX = tvec.at<double>(0);
		 double transY = tvec.at < double>(1);
		 double transZ = tvec.at<double>(2);

		 double rotX = rvec.at<double>(0);
		 double rotY = rvec.at<double>(1);
		 double rotZ = rvec.at<double>(2);
		
		 
		 vector<Point2f> reprojectedPoints;
		 projectPoints(objPoints, rvec, tvec, cameraMatrix, distCoeffs, reprojectedPoints);
		 // C++: void projectPoints(InputArray objectPoints, InputArray rvec, InputArray tvec, InputArray cameraMatrix, InputArray distCoeffs, OutputArray imagePoints, OutputArray jacobian = noArray(), double aspectRatio = 0)
		 int bp = 0;
	
	 }//end of contours.size>0
	 
imwrite("fred.png", mask);
imshow("Image", inimg);
waitKey(0);
return(0);
}

/*inimg = inframe.getCvBGR()
self.currentimagecount += 1
cv2.imwrite(imagefilename, inimg)
inimg = cv2.transpose(inimg)
inimg = cv2.flip(inimg, 1)
*//////

/*


## Process function with USB output
def process(self, inframe, outframe) :
	# Get the next camera image(may block until it is captured) and here convert it to OpenCV BGR.If you need a
	# grayscale image, just use getCvGRAY() instead of getCvBGR().Also supported are getCvRGB() and getCvRGBA() :
	# self.currentloopcount = self.currentloopcount + 1
# if self.currentloopcount==self.maxloopcount:
	#    self.currentimagecount = self.currentimagecount + 1
	#    self.currentloopcount = 0
#    if self.currentimagecount>self.maximagecount:
	#       self.currentimagecount = self.minimagecount
	# self.currentimagecount = 242

	imagefilename = "practice" + str(self.currentimagecount) + ".png"

	#  inimg = cv2.imread(imagefilename + )
	#  inimg = cv2.imread("practice30325.png")

	inimg = inframe.getCvBGR()
	self.currentimagecount += 1
	cv2.imwrite(imagefilename, inimg)
	inimg = cv2.transpose(inimg)
	inimg = cv2.flip(inimg, 1)



	# Start measuring image processing time(NOTE: does not account for input conversion time) :
	self.timer.start()

	lowColor = np.array([53, 20, 211])
	highColor = np.array([86, 255, 255])
	imghls = cv2.cvtColor(inimg, cv2.COLOR_BGR2HLS)


	mask = cv2.inRange(imghls, lowColor, highColor)

	contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	#now filter the contours

	biggestIndex = -1;
secondIndex = -1;
biggestSize = 0;

secondSize = 0;
index = 0

backtorgb = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
if len(contours) > 0:
for c in contours :
if cv2.contourArea(c) > biggestSize:
secondSize = biggestSize
secondIndex = biggestIndex
biggestSize = cv2.contourArea(c)
biggestIndex = index
#        cv2.putText(backtorgb, str(cv2.contourArea(c)), (3, 233), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255))
elif  cv2.contourArea(c) > secondSize:
secondSize = cv2.contourArea(c)
secondIndex = index
index = index + 1



if biggestIndex > -1:
cv2.drawContours(backtorgb, contours, biggestIndex, (0, 255, 0), 1)
brect1 = cv2.minAreaRect(contours[biggestIndex])
brectPoints = cv2.boxPoints(brect1)
brectPoints = np.int0(brectPoints)
cv2.drawContours(backtorgb, [brectPoints], 0, (0, 0, 255), 1)
boxText = "(" + str(brectPoints[0][0]) + "," + str(brectPoints[0][1]) + ")" + "(" + str(brectPoints[1][0]) + "," + str(brectPoints[1][1]) + ")""(" + str(brectPoints[2][0]) + "," + str(brectPoints[2][1]) + ")""(" + str(brectPoints[3][0]) + "," + str(brectPoints[3][1]) + ")"
#cv2.putText(backtorgb, boxText, (3, 233), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255))
if self.written == False:
self.datafile.write(boxText)
self.datafile.write("\n")
if secondIndex > -1:
cv2.drawContours(backtorgb, contours, secondIndex, (0, 255, 0), 1)
brect2 = cv2.minAreaRect(contours[secondIndex])
brectPoints2 = cv2.boxPoints(brect2)

brectPoints2 = np.int0(brectPoints2)
boxText = "(" + str(brectPoints2[0][0]) + "," + str(brectPoints2[0][1]) + ")" + "(" + str(brectPoints2[1][0]) + "," + str(brectPoints2[1][1]) + ")""(" + str(brectPoints2[2][0]) + "," + str(brectPoints2[2][1]) + ")""(" + str(brectPoints2[3][0]) + "," + str(brectPoints2[3][1]) + ")"
cv2.putText(backtorgb, boxText, (3, 233), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255))
cv2.drawContours(backtorgb, [brectPoints2], 0, (0, 0, 255), 1)
if self.written == False:
self.datafile.write(boxText)
self.datafile.write("\n")


#if you are here, there must be two contours.  Find the appropriate
#corners


v1 = 321 #there ought to be an easier way, but......
v2 = 321
v3 = 321
v4 = 321

v1i = -1
v2i = -1
v3i = -1
v4i = -1

#This is possibly the dumbest sort I've ever done.  But it works and I was tired.
#It is really a modification of some earlier code, that made sense.

for index in range(0, 4) :
	if brectPoints[index][1] < v1 :
		v4i = v3i
		v3i = v2i
		v2i = v1i
		v1i = index

		v4 = v3
		v3 = v2
		v2 = v1
		v1 = brectPoints[index][1]
		elif brectPoints[index][1] < v2:
v4i = v3i
v3i = v2i
v2i = index

v4 = v3
v3 = v2
v2 = brectPoints[index][1]
elif brectPoints[index][1] < v3:
v4i = v3i
v3i = index

v4 = v3
v3 = brectPoints[index][1]
	else:
v4i = index
v4 = brectPoints[index][1]


point1_1 = brectPoints[v1i]
point2_1 = brectPoints[v2i]
point3_1 = brectPoints[v3i]
point4_1 = brectPoints[v4i]


v1 = 321 #there ought to be an easier way, but......
v2 = 321
v3 = 321
v4 = 321

v1i = -1
v2i = -1
v3i = -1
v4i = -1

for index in range(0, 4) :
	if brectPoints2[index][1] < v1 :
		v4i = v3i
		v3i = v2i
		v2i = v1i
		v1i = index

		v4 = v3
		v3 = v2
		v2 = v1
		v1 = brectPoints2[index][1]
		elif brectPoints2[index][1] < v2:
v4i = v3i
v3i = v2i
v2i = index

v4 = v3
v3 = v2
v2 = brectPoints2[index][1]
elif brectPoints2[index][1] < v3:
v4i = v3i
v3i = index

v4 = v3
v3 = brectPoints2[index][1]
	else:
v4i = index
v4 = brectPoints2[index][1]


point1_2 = brectPoints2[v1i]
point2_2 = brectPoints2[v2i]
point3_2 = brectPoints2[v3i]
point4_2 = brectPoints2[v4i]


#Almost there - set up the arrays of object and image points
#cv2.putText(backtorgb, str(topcorner2[0]) + " " + str(topcorner2[1]), (3, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255))

#           objpoints = np.array(((-5.94, 0.5, 0), (-4, 0, 0), (4, 0, 0), (5.94, 0.5, 0)), dtype = np.float)3
x1 = point1_1[0]
x2 = point1_2[0]
imagepoints = np.array((point1_1, point2_1, point3_1, point4_1, point1_2, point2_2, point3_2, point4_2), dtype = np.float)

logstring(str(imagepoints))


if (x1 < x2) :
	objpoints = np.array(((-5.94, 0.5, 0), (-4, 0, 0), (-7.19, -4.34, 0), (-5.25, -4.84, 0), (5.94, 0.5, 0), (4, 0, 0), (7.19, -4.34, 0), (5.25, 4.84, 0)), dtype = np.float)
else:
objpoints = np.array(((5.94, 0.5, 0), (4, 0, 0), (7.19, -4.34, 0), (5.25, 4.84, 0), (-5.94, 0.5, 0), (-4, 0, 0), (-7.19, -4.34, 0), (-5.25, -4.84, 0)), dtype = np.float)
#  imagepoints = np.array(((50 * (-5.94) + 320, 50 * 0.5 + 240), (50 * (-4) + 320, 0 + 240), (50 * 4 + 320, 0 + 240), (50 * 5.94 + 320, 50 * 0.5 + 240)), dtype = np.float)
#  imagepoints = np.array(((104, 194), (124, 197), (195, 194), (214, 188)), dtype = np.float)
logstring(str(imagepoints))
logsttring("\n")
logstring(str(objpoints))
logstring("\n")
logstring("\n")
logstring("\n")


if self.written == False:
self.datafile.write("Image Points\n")
self.datafile.write(str(imagepoints[0][0]) + " " + str(imagepoints[0][1]) + "\n")
self.datafile.write(str(imagepoints[1][0]) + " " + str(imagepoints[1][1]) + "\n")
self.datafile.write(str(imagepoints[2][0]) + " " + str(imagepoints[2][1]) + "\n")
self.datafile.write(str(imagepoints[3][0]) + " " + str(imagepoints[3][1]) + "\n")


#imagepoints = np.array(((186, 220), (188, 212), (187, 171), (186, 164)), dtype = np.float)
cv2.putText(backtorgb, str(imagepoints[0][0]) + " " + str(imagepoints[0][1]), (3, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255))
cv2.putText(backtorgb, str(imagepoints[1][0]) + " " + str(imagepoints[1][1]), (3, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255))
cv2.putText(backtorgb, str(imagepoints[2][0]) + " " + str(imagepoints[2][1]), (3, 105), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255))
cv2.putText(backtorgb, str(imagepoints[3][0]) + " " + str(imagepoints[3][1]), (3, 125), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255))

#     cv2.putText(backtorgb, str(topcorner1[0]) + " " + str(topcorner1[1]), (160, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255))
#     cv2.putText(backtorgb, str(secondcorner1[0]) + " " + str(secondcorner1[1]), (160, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255))
#     cv2.putText(backtorgb, str(topcorner2[0]) + " " + str(topcorner2[1]), (160, 105), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255))
#     cv2.putText(backtorgb, str(secondcorner2[0]) + " " + str(secondcorner2[1]), (160, 125), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255))
#The moment of truth ?
errorestimate, rvec, tvec = cv2.solvePnP(objpoints, imagepoints, self.cameraMatrix, self.distcoeff)

#cv2.putText(backtorgb, str(tvec[0]) + " " + str(tvec[1]) + " " + str(tvec[2]), (3, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255))
cv2.putText(backtorgb, "%.2f" % tvec[0] + " " + "%.2f" % tvec[1] + " " + "%.2f" % tvec[2], (3, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255))

cv2.putText(backtorgb, "%.2f" % (rvec[0] * 180 / 3.14159) + " " + "%.2f" % (rvec[1] * 180 / 3.14159) + " " + "%.2f" % (rvec[2] * 180 / 3.14159), (3, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255))

#spit things out on the serial port, but first, do some testing.Print stuff out.


#change coordinate systems

ZYX, jac = cv2.Rodrigues(rvec)
#Now we have a 3x3 rotation matrix, and a translation vector.Form the 4x4 transformation matrix using homogeneous coordinates.
#There are probably numpy functions for array / matrix manipulations that would make this easier, but I don ? t know them and this works.
totaltransformmatrix = np.array([[ZYX[0, 0], ZYX[0, 1], ZYX[0, 2], tvec[0]], [ZYX[1, 0], ZYX[1, 1], ZYX[1, 2], tvec[1]], [ZYX[2, 0], ZYX[2, 1], ZYX[2, 2], tvec[2]], [0, 0, 0, 1]] )
#The resulting array is the transformation matrix from world coordinates(centered on the target) to camera coordinates. (Centered on the camera) We need camera to world.That is just the inverse of that matrix.
WtoC = np.mat(totaltransformmatrix)

inverserotmax = np.linalg.inv(totaltransformmatrix)
cv2.putText(backtorgb, "%.2f" % inverserotmax[0, 3] + " " + "%.2f" % inverserotmax[1, 3] + " " + "%.2f" % inverserotmax[2, 3], (3, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255))

processedFileName = "output" + str(self.currentimagecount - 1) + ".png"
cv2.imwrite(processedFileName, backtorgb)






# cv2.putText(outimg, fps, (3, height - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255))

# Convert our output image to video output format and send to host over USB :
outframe.sendCv(backtorgb)
self.written = True

def logstring(self, lstring) :
	self.datafile.write(lstring)

	def logstringonce(self, lstring) :
	if (self.written == False) :
		self.datafile.write(lstring)

		def writeToScreen(self, screenString, selectedImage, startX, startY) :
		cv2.putText(selectedImage, screenString, )(startX, startY), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255))

*/