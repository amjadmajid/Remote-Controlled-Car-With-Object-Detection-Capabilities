from MotorModule import Motor
import KeyPressModule as kp
import JoystickModule as js
import time
import cv2
from CameraModule import *
from datetime import datetime, timedelta
from picamera import PiCamera
from picamera.array import PiRGBArray
import imutils 
from imutils.video.pivideostream import PiVideoStream
from imutils.video import FPS

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
        time.sleep(.05)
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

captureTime = datetime.now() - timedelta(seconds=1)
def photoCaptureTime(timeInterval):
    global captureTime
    if captureTime <= datetime.now():
        captureTime = datetime.now() + timedelta(seconds=timeInterval)
        return True

    return False





def main():
    move()
    # reading images from the camera thread
    if photoCaptureTime(5):
        frame = vs.read()
        frame = imutils.resize(frame, width=400)
        objInfo = getObject(frame, draw=False, targets=['person'])
        if len(objInfo):
            print(objInfo[0][0])
        #cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        fps.update()

    #if photoCaptureTime(0.5):
        #success, img = cap.read()
        #objInfo = getObject(img, targets=['person'])
        #print(objInfo)
        #cv2.imshow("Output", img)

    #key = cv2.waitKey(1) & 0xff
    #if key == ord("q"):
        #break
    
        
if __name__ == '__main__':
    #cap = cv2.VideoCapture(0)
    vs = PiVideoStream().start()
    time.sleep(2.0)
    fps = FPS().start()
    while True:
        main()
    fps.stop()
    cv2.destroyAllWindows()
    vs.stop()