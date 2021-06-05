import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray
import imutils 
from imutils.video.pivideostream import PiVideoStream
from imutils.video import FPS
import time

# img = cv2.imread('Lenna.png')

classNames = []
classFile = '/home/pi/Desktop/self-driving/python-based-project/ObjectDetection/coco.names'
with open (classFile, 'rt') as f:
    classNames = f.read().strip().split('\n')
# print(classNames)

configPath = '/home/pi/Desktop/self-driving/python-based-project/ObjectDetection/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weightsPath = '/home/pi/Desktop/self-driving/python-based-project/ObjectDetection/frozen_inference_graph.pb'

net = cv2.dnn_DetectionModel(weightsPath,configPath)
net.setInputSize(320,320)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5,127.5))
net.setInputSwapRB(True)

def detectionCleanup():
    fps.stop()
    cv2.destroyAllWindows()
    vs.stop()
    
#def getObject(img, draw=True, targets=[]):
def getObject():
    print("objectDetection")
    draw=True
    targets=['person']
    vs = PiVideoStream(resolution=(320, 320), framerate=32).start()
    time.sleep(2.0)
    fps = FPS().start()
    
    while True:
        frame = vs.read()
        frame = imutils.resize(frame)
        
        classIds, confs, bbox = net.detect(frame, confThreshold=0.7, nmsThreshold=.2)
        objectInfo=[]
        className=None
        userDefCalsses=False
        if len(targets)==0: targets=classNames

        if len(classIds) !=0:
            for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
                    #print("classId=",classId, "classNames Len=", len(classNames))
                    className=classNames[classId-1]
                    if className in targets:
                        objectInfo.append((className,confidence,box))
                        if (draw):
                            cv2.rectangle(frame, box, color=(0,255,0), thickness=2)
                            if classId > 0:
                                cv2.putText(frame, className.upper(), (box[0]+10, box[1]+30),
                                            cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0),2)
                                cv2.putText(frame, str(round(confidence*100,2)), (box[0]+200, box[1]+30),
                                            cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),2)
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        fps.update()
        print(objectInfo)



if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    while True:
        success, img = cap.read()
        objInfo = getObject(img, targets=['person'])
        print(objInfo)
        cv2.imshow("Output", img)
        cv2.waitKey(1)
