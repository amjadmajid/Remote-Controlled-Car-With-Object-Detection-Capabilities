from MotorModule import Motor
import KeyPressModule as kp
import JoystickModule as js
from time import sleep
import cv2
from CameraModule import *

##############################
motor = Motor(12,5,6, 22,27,13)
movement = 'Joystick' 
##############################

#kp.init()

def main():

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
    
    success, img = cap.read()
    objInfo = getObject(img, targets=['cup'])
    #print(objInfo)
    cv2.imshow("Output", img)
    cv2.waitKey(1)
    
        
if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    while True:
        main()