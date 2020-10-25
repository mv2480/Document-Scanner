import cv2
import numpy as np

# define a video capture object
vid = cv2.VideoCapture(0)
vid.set(3, 640)
vid.set(4, 480)
vid.set(10, 150)

color = [[0, 0, 79, 123, 29, 255]]
myColorValues = [236, 245, 66]
myPoint = []
a,b,x1,y1,i = 0,0,0,0,0

def masking(colors, img):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    point = []
    lower = np.array(colors[0][0:3])
    upper = np.array(colors[0][3:6])
    mask = cv2.inRange(imgHSV, lower, upper)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.dilate(mask, kernel, iterations=2)
    x, y, w, h = shapedec(mask)
    cv2.rectangle(imgResult, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.putText(imgResult, "Press C ",
                (x + (w // 2) - 10, y + (h // 2) - 10), cv2.FONT_HERSHEY_COMPLEX, 0.7,
                (0, 0, 0), 2)
    if x!=0 and y!=0:
        point.append([x,y])
        point.append([x+w,y])
        point.append([x,y+h])
        point.append([x+w,y+h])

    if cv2.waitKey(1) & 0xFF == ord('c'):
        if len(point)!=0:
            for newP in point:
                myPoint.append(newP)
        if len(myPoint)!=0:
            cropImg(myPoint,frame)



def shapedec(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, w, h= 0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        print(area)
        if area>60000:
            cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 3)
            area = cv2.contourArea(cnt)
            area = cv2.contourArea(cnt)
            peri = cv2.arcLength(cnt, True)
            # print(peri)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            objCor = len(approx)
            x, y, w, h = cv2.boundingRect(approx)
    return x , y, w, h

def cropImg(mypoint, img):

    width, height = 560, 800
    pts1 = np.float32([mypoint[0], mypoint[1], mypoint[2], mypoint[3]])
    pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgOutput = cv2.warpPerspective(img, matrix, (width, height))
    imgCropped = imgOutput[20:imgOutput.shape[0] - 20, 20:imgOutput.shape[1] - 20]
    imgCropped = cv2.resize(imgCropped, (width, height))
    cv2.imshow('image', imgCropped)



while (True):

    # Capture the video frame
    # by frame

    success, frame = vid.read()
    imgResult = frame.copy()
    masking(color, frame)



    # Display the resulting frame
    cv2.imshow('frame', imgResult)

    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()
