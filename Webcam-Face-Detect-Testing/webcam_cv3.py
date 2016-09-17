import cv2
import sys
import logging as log
import datetime as dt
import decimal
import sys
sys.path.append('/Users/ericsu/HackCMU2016')
import test_pyautogui
import speech
import threading
import time
import pyautogui

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
    if (facex - avgx > 45): return "left"
    elif (facex - avgx < -45): return "right"
    elif (facey - avgy > 35): return "bottom"
    elif (facey - avgy > 15): return "midbottom"
    elif (facey - avgy < -30): return "top"
    elif (facey - avgy < -15): return "midtop"
    else: return "neutral"
    


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
eyesx = 0
eyesy = 0
eyesw = 0
eyesh = 0
frame = None

def headIsAtLocation(string):
    return headLocation( facex, facey) == string
'''
def drawRectangles():
    if (headIsAtLocation("right")):
        cv2.rectangle(frame, (facex, facey), (facex+facew, facey+faceh), (225, 0, 255), 2)
    elif (headIsAtLocation("left")):
        cv2.rectangle(frame, (facex, facey), (facex+facew, facey+faceh), (0, 0, 0), 2)
    elif (headIsAtLocation("top")):
        cv2.rectangle(frame, (facex, facey), (facex+facew, facey+faceh), (0, 0, 255), 2)
    elif (headIsAtLocation("midtop")):
        cv2.rectangle(frame, (facex, facey), (facex+facew, facey+faceh), (0, 255, 255), 2)
    elif (headIsAtLocation("midbottom")):
        cv2.rectangle(frame, (facex, facey), (facex+facew, facey+faceh), (255, 255, 0), 2)
    elif (headIsAtLocation("bottom")):
        cv2.rectangle(frame, (facex, facey), (facex+facew, facey+faceh), (0, 255, 0), 2)
    else:
        cv2.rectangle(frame, (facex, facey), (facex+facew, facey+faceh), (255, 255, 255), 2)
'''
def frameCapture():
    global anterior
    global captureCount
    global constantMinus
    global totalx
    global totaly
    global totalw
    global totalh
    global avgx
    global avgy
    global avgh
    global avgw
    global facex
    global facey
    global facew
    global faceh
    global eyesx
    global eyesy
    global eyesw
    global eyesh
    
    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    eyeCascade = cv2.CascadeClassifier('haarcascade_eye.xml')
    eyesCascade = cv2.CascadeClassifier('haarcascade_eyes.xml')
    #cascPath = sys.argv[1]
    #faceCascade.load('haarcascade_frontalface_default.xml')
    #faceCascade = cv2.CascadeClassifier(cascPath)
    log.basicConfig(filename='webcam.log',level=log.INFO)
    video_capture = cv2.VideoCapture(0)
    while True:
        # Capture frame-by-frame
        global frame
        ret, frame = video_capture.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
            # flags=cv2.cv.CV_HAAR_SCALE_IMAGE
        )

        faceh = 0
        facew = 0

        for (x, y, w, h) in faces:
            if (w * h > faceh * facew):
                facex = x
                facey = y
                facew = w
                faceh = h

        if (facew == 0):
            facew = 1

        if (faceh == 0):
            faceh = 1
        
        # EYES detection
        eyes_gray = gray[facey:facey+faceh, facex:facex+facew]
        eyes_color = frame[facey:facey+faceh, facex:facex+facew]
        eyes = eyesCascade.detectMultiScale(eyes_gray)

        for(x, y, w, h) in eyes:
            if (w > h and w * h > eyesh * eyesw):
            #if (w > eyesw):
                eyesx = x
                eyesy = y
                eyesh = h
                eyesw = w
            #cv2.rectangle(eyes_color,(eyesx,eyesy),(eyesx+eyesw,eyesy+eyesh),(0,255,0),2)

        if (eyesw == 0):
            eyesw = 1

        if (eyesh == 0):
            eyesh = 1

        newEyes = [[eyesx + int(eyesw / 8.5), eyesy + int(eyesh / 2.85), (eyesw // 4),int(eyesh /2.85)],
                   [eyesx + int((3 *eyesw) / 4) - (eyesw // 8),eyesy + int(eyesh / 2.85), (eyesw // 4), int(eyesh/2.85)]]

        #newEyes = [[eyesx, eyesy + int(faceh / 7), int(facew / 5), int(faceh / 10)],
#                   [eyesx + int((3 * facew) / 5), eyesy + int(faceh / 7), int(facew / 5), int(faceh / 10)]]

        for (x, y, w, h) in newEyes:
            cv2.rectangle(eyes_color, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        #cv2.rectangle(eyes_color,(eyesx + (eyesw // 8),eyesy),(eyesx+(eyesw // 4)+(eyesw // 8),eyesy+eyesh),(0,255,0),2)
        #cv2.rectangle(eyes_color,(eyesx + ((3 *eyesw) // 4) - (eyesw // 8),eyesy),(eyesx+eyesw - (eyesw // 8), eyesy+eyesh),(0,255,0),2)

        
        '''
        # EYE DETECTION
        toleranceM = 1.25
        toleranceA = 10
        roi_gray = gray[eyesy:eyesy+eyesh, eyesx:eyesx+eyesw]
        roi_color = frame[eyesy:eyesy+eyesh, eyesx:eyesx+eyesw]
        eye = eyeCascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eye:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
        '''
        

        
        
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

        #cv2.rectangle(frame, (avgx, avgy), (avgx+avgw, avgy+avgh), (0, 0, 0), 2)

        
        if (headIsAtLocation("right")):
            #test_pyautogui.rightTab(headIsAtLocation, ('right',))
            cv2.rectangle(frame, (facex, facey), (facex+facew, facey+faceh), (255, 0, 255), 2)
        elif (headIsAtLocation("left")):
            cv2.rectangle(frame, (facex, facey), (facex+facew, facey+faceh), (0, 0, 0), 2)
        elif (headIsAtLocation("top")):
            cv2.rectangle(frame, (facex, facey), (facex+facew, facey+faceh), (0, 0, 255), 2)
        elif (headIsAtLocation("midtop")):
            cv2.rectangle(frame, (facex, facey), (facex+facew, facey+faceh), (0, 255, 255), 2)
        elif (headIsAtLocation("midbottom")):
            cv2.rectangle(frame, (facex, facey), (facex+facew, facey+faceh), (255, 255, 0), 2)
        elif (headIsAtLocation("bottom")):
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

doInThread = True

if(doInThread):
    t = threading.Thread(target = frameCapture, args = ())
    t.daemon = True
    t.start()
    #t.join()

    #time.sleep(3)

    while(True):
        if (headIsAtLocation("right")):
                test_pyautogui.rightTab(headIsAtLocation, ('right',))
        if (headIsAtLocation("left")):
                test_pyautogui.leftTab(headIsAtLocation, ('left',))
        if (headIsAtLocation("midtop")):
                #print("midtop")
                test_pyautogui.scroll(3, 0, headIsAtLocation, ('midtop',))
        if (headIsAtLocation("top")):
                #print("top")
                test_pyautogui.scroll(3, 4, headIsAtLocation, ('top',))
        if (headIsAtLocation("midbottom")):
                #print("midtop")
                test_pyautogui.scroll(-3, 0, headIsAtLocation, ('midbottom',))
        if (headIsAtLocation("bottom")):
                #print("top")
                test_pyautogui.scroll(-3, -4, headIsAtLocation, ('bottom',))
else:
    #speech.listen()
    frameCapture()

print(avgx)
