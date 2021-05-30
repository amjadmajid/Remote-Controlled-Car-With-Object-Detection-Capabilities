from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

#initialize the camera and get a reference to the raw camera capture
cam  = PiCamera()
cam.resolution=(640,480)
cam.framerate=1
rawCapture = PiRGBArray(cam, size=(640,480))

# allow the camera to warmup
time.sleep(0.1)

# capture an  image
#cam.capture(rawCapture, format="bgr")
for frame in cam.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    #
    img = frame.array

    #display the image using OpenCV `imshow` method
    cv2.imshow("Image", img)
    key = cv2.waitKey(1) & 0xff
    rawCapture.truncate(0)
    #keep the image on screen until a key is pressed 
    if key == ord("q"):
        break

