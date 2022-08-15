from imutils.video.pivideostream import PiVideoStream
from imutils.video import FPS
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import imutils 
import cv2

# initialize the camera and stream
vs = PiVideoStream().start()
time.sleep(2.0)
fps = FPS().start()
while True: 
    frame = vs.read()
    frame = imutils.resize(frame, width=400)
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    fps.update()
fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
cv2.destroyAllWindows()
vs.stop()