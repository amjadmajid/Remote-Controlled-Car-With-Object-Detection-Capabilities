from MotorModule import Motor
import KeyPressModule as kp
import JoystickModule as js
import time
import cv2
from CameraModule import *
from datetime import datetime, timedelta
from multiprocessing  import Process


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
    objDetect = ObjectDetect()
    process = Process(target=objDetect.getObject)
    process.start()
    while True: 
        move()

        
        
if __name__ == '__main__':
    #cap = cv2.VideoCapture(0)
    main()
    detectionCleanup()
    
