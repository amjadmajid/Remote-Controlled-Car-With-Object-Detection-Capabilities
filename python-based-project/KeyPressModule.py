import pygame as pg

def init():
    pg.init()
    win = pg.display.set_mode((100,100))

def getKey(keyName):
    ans = False
    while True:
        for eve in pg.event.get():pass
        keyInput = pg.key.get_pressed()
        pressedKey = getattr(pg, 'K_{}'.format(keyName))
        if keyInput[pressedKey]:
            ans = True
        pg.display.update()
        return ans
    
def main():
    if getKey('LEFT'):
        print('Key left was pressed')
    if getKey('RIGHT'):
        print('Key right was pressed')
        
if __name__=='__main__':
    init()
    while True:
        main()
