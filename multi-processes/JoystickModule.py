import pygame as pg
from time import sleep
pg.init()
controller = pg.joystick.Joystick(0)
controller.init()

buttons = {'x':0, 'o':0, 't':0,'s':0,
           'L1':0,'R1':0, 'L2':0,'R2':0,
           'share':0,'options':0,
           'axis1':0., 'axis2':0.,'axis3':0., 'axis4':0.}
axiss=[0.,0.,0.,0.,0.,0.,]

def getJS(name=''):
    global buttons
    #retrieve any event ...
    for event in pg.event.get():
        if event.type == pg.JOYAXISMOTION:           # Analog Stick values
            axiss[event.axis] = round(event.value,2)
        elif event.type == pg.JOYBUTTONDOWN:     # When button pressed
            #print(event.dict,event.joy, event.button, 'PRESSED')
            for x, (key,val) in enumerate(buttons.items()):
                if x <10:
                    if controller.get_button(x):buttons[key]=1
        elif event.type == pg.JOYBUTTONUP:
            #print(event.dict,event.joy, event.button, 'PRESSED')
            for x, (key,val) in enumerate(buttons.items()):
                if x <10:
                    if event.button==x:buttons[key]=0
    # to remove element 2 since axis numbers are 01234
    buttons['axis1'],buttons['axis2'],buttons['axis3'],buttons['axis4'] =\
                                [axiss[0],axiss[1],axiss[3],axiss[4]]
    
    if name == '':
        return buttons
    else:
    
        return buttons[name]

def main():
    print(getJS()) # to get all values
    sleep(.05)
    
if __name__=="__main__":
    while True:
        main()
                    
            