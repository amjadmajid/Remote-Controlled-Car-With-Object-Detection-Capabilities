from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

#initialize the camera and get a reference to the raw camera capture
with PiCamera() as cam:
    cam.resolution=(640,480)

    with PiRGBArray(cam, size=(640,480)) as output:
        # capture an  image
        cam.capture(output, format="bgr")
        img = output.array

        #display the image using OpenCV `imshow` method
        cv2.imshow("Image", img)
        key = cv2.waitKey(0) 
