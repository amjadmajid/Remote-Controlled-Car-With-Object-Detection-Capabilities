import cv2
import time
from picamera import PiCamera
from picamera.array import PiRGBArray
import imutils 
from imutils.video import FPS
from imutils.video.pivideostream import PiVideoStream
from multiprocessing  import Process

def callObjDetectProcess():
    objDetect = ObjectDetect()
    process = Process(target=objDetect.getObject)
    process.start()

class ObjectDetect():
    def __init__(self, resolution=(320,240), framerate=32, draw=True, targets=['person']):
        print("objectDetect")

        self.targets = targets
        self.draw = draw
        self.classNames = []
        classFile = '/home/pi/Desktop/self-driving/python-based-project/ObjectDetection/coco.names'
        with open (classFile, 'rt') as f:
            self.classNames = f.read().strip().split('\n')

        configPath = '/home/pi/Desktop/self-driving/python-based-project/ObjectDetection/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
        weightsPath = '/home/pi/Desktop/self-driving/python-based-project/ObjectDetection/frozen_inference_graph.pb'

        self.net = cv2.dnn_DetectionModel(weightsPath,configPath)
        self.net.setInputSize(resolution[0],resolution[1])
        self.net.setInputScale(1.0/ 127.5)
        self.net.setInputMean((127.5, 127.5,127.5))
        self.net.setInputSwapRB(True)

        self.vs = PiVideoStream(resolution, framerate=framerate).start()
        time.sleep(2.0)
        self.fps = FPS().start()

    def detectionCleanup(self):
        self.fps.stop()
        cv2.destroyAllWindows()
        self.vs.stop()
        
    def getObject(self):

        while True:
            frame = self.vs.read()
            frame = imutils.resize(frame)
            print("reading new frame") 
            classIds, confs, bbox = self.net.detect(frame, confThreshold=0.7, nmsThreshold=.2)
            objectInfo=[]
            className=None
            if len(self.targets)==0: self.targets=classNames

            if len(classIds) !=0:
                for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
                        #print("classId=",classId, "classNames Len=", len(classNames))
                        className=self.classNames[classId-1]
                        if className in self.targets:
                            objectInfo.append((className,confidence,box))
                            if (self.draw):
                                cv2.rectangle(frame, box, color=(0,255,0), thickness=2)
                                if classId > 0:
                                    cv2.putText(frame, className.upper(), (box[0]+10, box[1]+30),
                                                cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0),2)
                                    cv2.putText(frame, str(round(confidence*100,2)), (box[0]+200, box[1]+30),
                                                cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),2)
            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1) & 0xFF
            self.fps.update()
            
            print(objectInfo)

if __name__ == "__main__":
    objDetect = ObjectDetect()
    while True:
        objDetect.getObject()
    objDetect.detectionCleanup(self)

