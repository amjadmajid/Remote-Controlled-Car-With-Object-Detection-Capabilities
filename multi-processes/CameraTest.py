import cv2

# Define GStreamer pipeline string
gst_pipeline = 'libcamerasrc ! video/x-raw,format=BGR,width=640,height=480,framerate=30/1 ! videoconvert ! appsink'

cap = cv2.VideoCapture(gst_pipeline, cv2.CAP_GSTREAMER)
if not cap.isOpened():
    print("Failed to open camera")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to get frame")
        break

    cv2.imshow('Camera', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


