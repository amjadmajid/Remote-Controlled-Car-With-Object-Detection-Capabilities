from MotorModule import Motor
import KeyPressModule as kp
import JoystickModule as js
import time
import cv2
from CameraModule import *
from datetime import datetime, timedelta


##############################
motor = Motor(13,5,6, 27,17,12)
movement = 'Joystick' 
##############################

def move():
    if movement == 'Joystick':
        jsVal = js.getJS()
        # print(jsVal)
        # print()
        #print(-jsVal['axis2'])

        motor.move(jsVal['axis1'],-jsVal['axis2'] * .94 ,0.1)
        time.sleep(.05)

            
    else:
        if kp.getKey('UP'):
            motor.move(1,0,.1)
        elif kp.getKey('DOWN'):
            motor.move(-1,0,.1) 
        elif kp.getKey('LEFT'):
            motor.move(1,1,.1) 
        elif kp.getKey('RIGHT'):
            motor.move(1,-1,.1) 
        else:
            motor.stop(.1)

# captureTime = datetime.now() - timedelta(seconds=1)
# def photoCaptureTime(timeInterval):
#     global captureTime
#     if captureTime <= datetime.now():
#         captureTime = datetime.now() + timedelta(seconds=timeInterval)
#         return True
#     return False

def main():
    while True: 
        move()

        
if __name__ == '__main__':
    # objDetect = ObjectDetect()
    # process = Process(target=objDetect.getObject)
    # process.start()
    main()
    # motor.move(1,0,10)

    
