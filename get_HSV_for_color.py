import cv2
import numpy as np

cap = cv2.VideoCapture(0)

cv2.namedWindow('configure MinMax HSV')

def nothing(x):
    pass

erode_dialate_kernel = np.ones((5,5), np.uint8)
HSV_minmax = ['HMin','SMin','VMin','HMax','SMax','VMax']
value = [179,255,255,179,255,255]

for string,val in zip(HSV_minmax,value):
    cv2.createTrackbar(string, 'configure MinMax HSV', 0, val,nothing)
    
cv2.setTrackbarPos('HMax', 'configure MinMax HSV', 179)
cv2.setTrackbarPos('SMax', 'configure MinMax HSV', 255)
cv2.setTrackbarPos('VMax', 'configure MinMax HSV', 255)

# Initialize HSV min/max values
hMin = sMin = vMin = hMax = sMax = vMax = 0


while True:
    _,frame = cap.read()
    frame = cv2.resize(frame,(650,500))
    blurred = cv2.GaussianBlur(frame, (15,15),0)
    hsv = cv2.cvtColor(blurred,cv2.COLOR_BGR2HSV)

    hMin = cv2.getTrackbarPos('HMin', 'configure MinMax HSV')
    sMin = cv2.getTrackbarPos('SMin', 'configure MinMax HSV')
    vMin = cv2.getTrackbarPos('VMin', 'configure MinMax HSV')
    hMax = cv2.getTrackbarPos('HMax', 'configure MinMax HSV')
    sMax = cv2.getTrackbarPos('SMax', 'configure MinMax HSV')
    vMax = cv2.getTrackbarPos('VMax', 'configure MinMax HSV')
    
    lower = np.array([hMin, sMin, vMin])
    upper = np.array([hMax, sMax, vMax])
    
    mask = cv2.inRange(hsv, lower,upper)
    mask = cv2.erode(mask,erode_dialate_kernel,iterations=2)
    mask = cv2.dilate(mask,erode_dialate_kernel,iterations=2)

    
    #cv2.imshow("main frame",frame)
    cv2.imshow("mask",mask)
    cv2.imshow("blur",blurred)

    if cv2.waitKey(1) & 0xff == ord("q"):
        break

    
print(lower,upper)
cap.release()
cv2.destroyAllWindows()
