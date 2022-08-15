from gpiozero import Button
from time import sleep

button = Button(2)

while True:
    print(button.is_pressed)
    sleep(.01)
    