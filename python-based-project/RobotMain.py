from MotorModule import Motor
import KeyPressModule as kp

##############################
motor = Motor(12,5,6, 22,27,13)
##############################

kp.init()

def main():
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
        
if __name__ == '__main__':
    while True:
        main()