from MotorModule import Motor
import KeyPressModule as kp
import JoystickModule as js
from time import sleep
import cv2
from CameraModule import *
from datetime import datetime, timedelta

##############################
motor = Motor(12,5,6, 22,27,13)
movement = 'Joystick' 
##############################

#kp.init()

def move():
    if movement == 'Joystick':
    jsVal = js.getJS()
    #print(jsVal)
    motor.move(-jsVal['axis2'],jsVal['axis1'],0.1)
    sleep(.05)
else:
    if kp.getKey('UP'):
        motor.move(0.8,0,.1)
    elif kp.getKey('DOWN'):
        motor.move(-0.8,0,.1) 
    elif kp.getKey('LEFT'):
        motor.move(0.5,0.6,.1) 
    elif kp.getKey('RIGHT'):
        motor.move(0.5,-0.6,.1) 
    else:
        motor.stop(.1)

captureFlag = True
def photoCaptureTime(frame, rawCapture):
    if captureFlag == True:
        captureTime = datetime.now() + timedelta(seconds=1)
        captureFlag = False
        img = frame.array
        #display the image using OpenCV `imshow` method
        objInfo = getObject(img)
        cv2.imshow("Image", img)
        key = cv2.waitKey(1) & 0xff
        rawCapture.truncate(0)
    if captureTime <= datetime.now():
        captureFlag=True



def main():

    #initialize the camera and get a reference to the raw camera capture
    cam  = PiCamera()
    cam.resolution=(320,320)
    cam.framerate=1
    rawCapture = PiRGBArray(cam, size=(320,320))

    # allow the camera to warmup
    time.sleep(0.1)
    for frame in cam.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        move()
        photoCaptureTime(frame, rawCapture)
        #keep the image on screen until a key is pressed 
        if key == ord("q"):
            break
    
        
if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    while True:
        main()