import cv2
import mediapipe as mp
import time
import math
import HandTrackingModule as htm
import subprocess
import numpy as np


wcam,hcam=640,480
ptime=0
ctime=0
cap=cv2.VideoCapture(0)


cap.set(3,wcam)
cap.set(4,hcam)
detector=htm.HandDetector(detectionCon=0.7)

minVol = 0
maxVol = 100
lastVol=-1
#using osascript to control the volume on macOS

def set_volume(vol_percent):
    vol_percent = max(0, min(100, int(vol_percent)))#changing the volume_percentage as the vol_percentage changes 
    script = f"set volume output volume {vol_percent}"
    subprocess.run(["osascript", "-e", script])#changes the volume using osascript commandof the system 


while True :
    success,img=cap.read()
    img=detector.findHands(img,draw=True) 
    lmlist=detector.findPosition(img,draw=False) 

#we know that 4 and 8 are used for thumb and index finger respectively
    if len(lmlist) !=0:
        #coordinates of thumb and index finger
        x1,y1=lmlist[4][1],lmlist[4][2] 
        x2,y2=lmlist[8][1],lmlist[8][2]
        cx,cy=(x1+x2)//2,(y1+y2)//2

        cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)  
        cv2.circle(img,(x2,y2),15,(255,0,255),cv2.FILLED) 
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)  
        cv2.circle(img,(cx,cy),15,(255,0,255),cv2.FILLED)

        length=math.hypot(x2-x1,y2-y1)
        print(int(length))

        vol = np.interp(length, [20, 200], [minVol, maxVol]) #interpolation of the length of the line between thumb and index finger to volume
        vol = int(vol)

        volBar = np.interp(length, [20, 200], [400, 150]) 
        cv2.rectangle(img, (50, 150), (85, 400), (0, 0, 0), 2)  
        cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)  
        cv2.putText(img, f'{vol} %', (40, 430), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)


        if vol != lastVol:
            set_volume(vol)
            print(f"Volume set to: {vol}%")
            lastVol = vol

        if length<50:
            cv2.circle(img,(cx,cy),15,(0,255,0),cv2.FILLED)

    

    ctime = time.time() 
    fps = 1 / (ctime - ptime)  
    ptime = ctime  
    # cv2.putText(img,f'Fps:{int(fps)}',(40,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),3)
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break