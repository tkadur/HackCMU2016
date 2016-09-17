import cv2
import sys
import logging as log
import datetime as dt
import decimal

def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

#'''
def keepGoing(position):
    if (position == headLocation( facex, facey)):
        return True
    else:
        return False
#'''
    

def headLocation( facex, facey):
    if (facex - avgx > 35): return "left"
    elif (facex - avgx < -35): return "right"
    elif (facey - avgy > 35): return "top"
    elif (facey - avgy > 15): return "midtop"
    elif (facey - avgy < -30): return "bottom"
    elif (facey - avgy < -10): return "midbottom"
    else: return "neutral"
    



faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eyeCascade = cv2.CascadeClassifier('haarcascade_eyes.xml')
#cascPath = sys.argv[1]
#faceCascade.load('haarcascade_frontalface_default.xml')
#faceCascade = cv2.CascadeClassifier(cascPath)
log.basicConfig(filename='webcam.log',level=log.INFO)

video_capture = cv2.VideoCapture(0)
anterior = 0

captureCount = 0
constantMinus = 5
totalx = 0
totaly = 0
totalw = 0
totalh = 0
avgx = 0
avgy = 0
avgh = 0
avgw = 0
facex = 0
facey = 0
facew = 0
faceh = 0

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
        # flags=cv2.cv.CV_HAAR_SCALE_IMAGE
    )

    

    # Draw a rectangle around the faces

    
    for (x, y, w, h) in faces:
        if (w * h > faceh * facey):
            facex = x
            facey = y
            facew = w
            faceh = h

    if (facew == 0):
        facew = 1

    if (faceh == 0):
        faceh = 1
            
    roi_gray = gray[facey:facey+faceh, facex:facex+facew]
    roi_color = frame[facey:facey+faceh, facex:facex+facew]
    #print(roi_gray)
    eyes = eyeCascade.detectMultiScale(roi_gray)
    for (ex,ey,ew,eh) in eyes:
        # Check eye validity
        centerx = ex + int(ew * 0.5)
        centery = ey + int(eh * 0.5)
        cond1 = (centerx > facex and centerx < facex + facew) and (centery > facey and centery < facey + faceh)
        '''
        print(centerx)
        print
        print(facex)
        '''
        cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
        
    captureCount += 1
    if (captureCount > constantMinus and captureCount <= constantMinus + 4):
        totalx += facex
        totaly += facey
        avgx = roundHalfUp(totalx / (captureCount - constantMinus))
        avgy = roundHalfUp(totaly / (captureCount - constantMinus))
        avgw = roundHalfUp(totalw / (captureCount - constantMinus))
        avgh = roundHalfUp(totalh / (captureCount - constantMinus))

    """
    print(avgy)
    print
    print(avgx)
    """

    cv2.rectangle(frame, (avgx, avgy), (avgx+avgw, avgy+avgh), (0, 0, 0), 2)


    if (headLocation( facex, facey) == "right"):
        cv2.rectangle(frame, (facex, facey), (facex+facew, facey+faceh), (225, 0, 255), 2)
    elif (headLocation( facex, facey) == "left"):
        cv2.rectangle(frame, (facex, facey), (facex+facew, facey+faceh), (0, 0, 0), 2)
    elif (headLocation( facex, facey) == "top"):
        cv2.rectangle(frame, (facex, facey), (facex+facew, facey+faceh), (0, 0, 255), 2)
    elif (headLocation( facex, facey) == "midtop"):
        cv2.rectangle(frame, (facex, facey), (facex+facew, facey+faceh), (0, 255, 255), 2)
    elif (headLocation( facex, facey) == "midbottom"):
        cv2.rectangle(frame, (facex, facey), (facex+facew, facey+faceh), (255, 255, 0), 2)
    elif (headLocation( facex, facey) == "bottom"):
        cv2.rectangle(frame, (facex, facey), (facex+facew, facey+faceh), (0, 255, 0), 2)
    else:
        cv2.rectangle(frame, (facex, facey), (facex+facew, facey+faceh), (255, 255, 255), 2)

    if anterior != len(faces):
        anterior = len(faces)
        log.info("faces: "+str(len(faces))+" at "+str(dt.datetime.now()))

    # Display the resulting frame
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
