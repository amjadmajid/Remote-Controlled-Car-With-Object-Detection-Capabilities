from flask import Flask, Response
import cv2

app = Flask(__name__)

# Initialize the camera
gst_pipeline = (
    'libcamerasrc ! '
    'video/x-raw,format=BGR,width=704,height=320,framerate=15/1 ! '
    'videoconvert ! appsink'
)
cap = cv2.VideoCapture(gst_pipeline, cv2.CAP_GSTREAMER)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

def generate_frames():
    global cap
    while True:
        success, frame = cap.read()
        if not success:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 70])
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return "Camera Feed"

if __name__ == "__main__":
    try:
        app.run(host='0.0.0.0', port=8080, threaded=True)
    finally:
        cap.release()

