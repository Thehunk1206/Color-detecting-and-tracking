import cv2
import numpy as np
import imutils

cap = cv2.VideoCapture(0)

erode_dialate_kernel = np.ones((5,5), np.uint8)

lower = np.array([5, 60, 134])
upper = np.array([61, 255, 255])

while True:
    _,frame = cap.read()
    frame = cv2.flip(frame,1)
    frame = cv2.resize(frame,(650,500))
    blurred = cv2.GaussianBlur(frame, (15,15),0)
    hsv = cv2.cvtColor(blurred,cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, lower,upper)
    mask = cv2.erode(mask,erode_dialate_kernel,iterations=2)
    mask = cv2.dilate(mask,erode_dialate_kernel,iterations=2)

    contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_NONE)
    contours = imutils.grab_contours(contours)
    Cx = None
    Cy = None
    if len(contours)>1:
        c = max(contours, key=cv2.contourArea)
        ((x,y),radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        (Cx,Cy) = (int(M["m10"]/M["m00"]),int(M["m01"]/M["m00"]))
        if radius>10:
            cv2.circle(frame,(Cx,Cy),2,(0,255,0),10)
            print(f"center cordinate {center}")
            
    cv2.imshow("main frame",frame)
    cv2.imshow("mask",mask)
    cv2.imshow("blur",blurred)

    if cv2.waitKey(1) & 0xff == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

