#include <opencv2/opencv.hpp>
#include <raspicam_cv.h>
#include <iostream>
#include <chrono>
#include <ctime>
#include <wiringPi.h>
 
using namespace std;
using namespace cv;
using namespace raspicam;

Mat frame, Matrix, framePers, frameGray, frameThesh, frameEdge, frameFinal;
Mat frameFinalDuplicate; // `Rect` function draws on the frame. We use this duplicate
                          // to not distort the frameFinal. See the function `Histogram`.
Mat ROILane;
vector<int> histogramLane;

int LeftLanePos, RightLanePos, Result;
stringstream ss;

RaspiCam_Cv Camera;  // create an object to access the raspberry pi class functionality
Point2f Source[] = {Point2f(50,160), Point2f(550,160), Point2f(0,240), Point2f(600,240)};
Point2f Destination[] = {Point2f(100,0), Point2f(500,0), Point2f(100,240), Point2f(500,240)};

void Setup(int argc, char **argv, RaspiCam_Cv &Camera){
  Camera.set(CAP_PROP_FRAME_WIDTH, ("-w", argc,argv,600));
  Camera.set(CAP_PROP_FRAME_HEIGHT, ("-h",argc,argv,240));
  Camera.set(CAP_PROP_BRIGHTNESS, ("-br",argc,argv,50));
  Camera.set(CAP_PROP_CONTRAST, ("-co",argc,argv,80));
  Camera.set(CAP_PROP_SATURATION, ("-sa", argc,argv,50));
  Camera.set(CAP_PROP_GAIN, ("-g", argc,argv,50));
  Camera.set(CAP_PROP_FPS, ("-fps", argc, argv,0)); // 0 means the camera will try to capture as many frame per second as possible.
}

void Capture(){
  Camera.grab();
  Camera.retrieve(frame);
  // by default opencv processes the images by bgr color space but not in rgb color space
  cvtColor(frame, frame, COLOR_BGR2RGB); // cvtColor(input, output, -), we are overwriting the frame variable.
}

void Perspective(){
  line(frame,Source[0], Source[1], Scalar(255,0,0));
  line(frame,Source[1], Source[3], Scalar(0,255,0));
  line(frame,Source[3], Source[2], Scalar(0,0,255));
  line(frame,Source[2], Source[0], Scalar(0,0,255));
  
  Matrix = getPerspectiveTransform(Source, Destination);
  warpPerspective(frame, framePers, Matrix, Size(500,240));
}

void Threshold(){
  cvtColor(framePers, frameGray, COLOR_RGB2GRAY);
  inRange(frameGray, 240, 255, frameThesh);  // inRange(gray_scale_input_image, below_this_vlaue_is_black, equal_or_above_is_white, output_white_black_image);
  Canny(frameGray, frameEdge, 500,700,3,false);
  add(frameThesh, frameEdge, frameFinal);
  cvtColor(frameFinal, frameFinalDuplicate, COLOR_GRAY2RGB);
  cvtColor(frameFinal, frameFinal, COLOR_GRAY2RGB);
  
}

void Histogram(){
    int frameWidth = 400; //frame.size().width; // frame.size().width = 500
    histogramLane.resize(frameWidth);
    histogramLane.clear();
    
    for (int i=0; i <frameWidth; i++){ 
      ROILane = frameFinalDuplicate(Rect(i,140,1,100));
      divide(255, ROILane, ROILane);
      histogramLane.push_back((int)(sum(ROILane)[0]));
    }
}

void LaneFinder(){
  vector<int>:: iterator LeftPtr;
  LeftPtr = max_element(histogramLane.begin(),  histogramLane.begin()+200);
  LeftLanePos = distance(histogramLane.begin(), LeftPtr);
  
  vector<int>:: iterator RightPtr;
  RightPtr = max_element(histogramLane.begin()+250,  histogramLane.end());
  RightLanePos = distance(histogramLane.begin(), RightPtr);
  
  line(frameFinal, Point2f(LeftLanePos,0), Point2f(LeftLanePos,240), Scalar(0,255,0), 3);
  line(frameFinal, Point2f(RightLanePos,0), Point2f(RightLanePos,240), Scalar(0,255,0), 3);
}

void LaneCenter()
{
  int laneCenter = (LeftLanePos + RightLanePos)/2;
  line (frameFinal, Point2f(laneCenter, 0), Point2f(laneCenter, 240), Scalar(0,255,0), 3);
  
  int frameCenter = 174;
  line (frameFinal, Point2f(frameCenter, 0), Point2f(frameCenter, 240), Scalar(0,0,255), 3);
  
  Result = laneCenter - frameCenter;
}

void WriteToFrame(){
  ss.str(" ");
  ss.clear();
  ss<<"Result= " << Result;
  putText(frame, ss.str(), Point2f(1,50), 0,1, Scalar(0,0,255), 2);
} 
void ImageShow(String label, Mat frame, int x, int y){
  namedWindow(label, WINDOW_KEEPRATIO);
  moveWindow(label, x,y);
  resizeWindow(label, 640, 480);
  imshow(label, frame);
}

void FramePerSecond(auto start,auto end){
    std::chrono::duration<double> elapsed_seconds = end-start;
    float t = elapsed_seconds.count();
    int FPS = 1/t;
    cout<<"FPS= "<< FPS<<endl;
}
 
void _Steering(int a, int b, int c, int d){
  digitalWrite(21, a);
  digitalWrite(22, b);
  digitalWrite(23, c);
  digitalWrite(24, d);
  
  cout<<"Steering =" << 8*d +4*c+2*b+a << endl;
}

void Steering(int Result)
{
	if(Result ==0){ 
      _Steering(0,0,0,0);  // decimal 0
      cout<<"Forward"<<endl;
      }
    else if( Result > 0 && Result < 10){
      _Steering(1,0,0,0);  // decimal 1
      cout<<"Right 1"<<endl;
    }
    else if( Result >= 10 && Result < 20){
      _Steering(0,1,0,0); // decimal 2
      cout<<"Right 2"<<endl;
    }
    else if( Result >= 20 ){
      _Steering(1,1,0,0);  // decimal 3
      cout<<"Right 3"<<endl; 
    } 
    else if( Result < 0 && Result > -10){
      _Steering(0,0,1,0);  // decimal 4
      cout<<"Left 1"<<endl;
    }
    else if( Result <= -10 && Result > -20){
      _Steering(1,0,1,0); // decimal 5
      cout<<"Left 2"<<endl;
    }
    else if( Result <= -20 ){
      _Steering(0,1,1,0);  // decimal 6
      cout<<"Left 3"<<endl;
    }

}
 
 
int main(int argc, char **argv){
  
  wiringPiSetup();
  pinMode(21, OUTPUT);
  pinMode(22, OUTPUT);
  pinMode(23, OUTPUT);
  pinMode(24, OUTPUT);
  
  Setup(argc, argv,Camera);
  if(! Camera.open()){  // Camera.open() return 1 if there is a connection to 
                        // the camera
      cout<< "Failed to connect"<<endl;
      return -1;
  }        
  cout<< "Camera ID" << Camera.getId()<<endl;

  while(1){
    auto start = std::chrono::system_clock::now();
    Capture();
    Perspective();
    Threshold();
    Histogram();
    LaneFinder();
    LaneCenter();
    WriteToFrame();
    Steering(Result);
  
  
    auto end = std::chrono::system_clock::now();
    FramePerSecond(start, end);
    ImageShow("RGB", frame, 10,100);
    ImageShow("Perspective", framePers, 650, 100);
    ImageShow("Gray", frameFinal, 1300, 100);
    

    waitKey(1);
  }
  return 0;
}


























