import cv2
frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
while True:
	success, img = cap.read()
	if success:
		cv2.imshow("Result", img)
	if cv2.waitKey(1) & 0xff == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()

