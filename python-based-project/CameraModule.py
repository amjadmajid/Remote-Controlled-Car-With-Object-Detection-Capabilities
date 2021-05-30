import cv2

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

def getObject(img, draw=True, targets=[]):
    classIds, confs, bbox = net.detect(img, confThreshold=0.7, nmsThreshold=.2)
    objectInfo=[]
    className=None
    userDefCalsses=False
    if len(targets)==0: targets=classNames

    if len(classIds) !=0:
        for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
                #print("classId=",classId, "classNames Len=", len(classNames))
                className=classNames[classId-1]
                if className in targets:
                    objectInfo.append( (className,confidence,box))
                    if (draw):
                        cv2.rectangle(img, box, color=(0,255,0), thickness=2)
                        if classId > 0:
                            cv2.putText(img, className.upper(), (box[0]+10, box[1]+30),
                                        cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0),2)
                            cv2.putText(img, str(round(confidence*100,2)), (box[0]+200, box[1]+30),
                                        cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),2)
    return objectInfo



if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    while True:
        success, img = cap.read()
        objInfo = getObject(img, targets=['person'])
        print(objInfo)
        cv2.imshow("Output", img)
        cv2.waitKey(1)
