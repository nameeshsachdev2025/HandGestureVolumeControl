import cv2 
import mediapipe as mp
import time
#will work as a module for hand detection

class HandDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode=mode
        self.maxHands=maxHands
        self.detectionCon=detectionCon
        self.trackCon=trackCon

        self.mpHands = mp.solutions.hands
        self.hands=self.mpHands.Hands(static_image_mode=self.mode,#constructor for the Hands class
            max_num_hands=self.maxHands,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon)
        self.mpDraw=mp.solutions.drawing_utils

    def findHands(self,img,draw=True):
        imgRGB=cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
        self.results = self.hands.process(imgRGB) 
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img,handLms,self.mpHands.HAND_CONNECTIONS)
        return img
    
    def findPosition(self,img,handNo=0,draw=True):
        lmList=[]
        if self.results.multi_hand_landmarks:   
              my_hand=self.results.multi_hand_landmarks[handNo]#for getting the specific hand
              for id,lm in enumerate(my_hand.landmark):
                    h,w,c=img.shape
                    cx,cy=int(lm.x*w),int(lm.y*h)
                    lmList.append([id,cx,cy])
                    if draw:
                        cv2.circle(img,(cx,cy),10,(255,0,255),cv2.FILLED)
        return lmList
    
def main():
    ptime=0
    ctime=0
    cap = cv2.VideoCapture(0)
    detector = HandDetector()
    while True:
        success,img= cap.read()
        img=detector.findHands(img,draw=True) #find hands in the image
        lmlist=detector.findPosition(img,draw=True) #find the position of the landmarks

        if len(lmlist) != 0:# if no hands are detected, lmlist will be empty
            print(lmlist[4]) #printing the position of the 5th landmark (thumb tip)
        ctime = time.time() #current time
        fps = 1 / (ctime - ptime) #calculating the frames per second
        ptime = ctime #previous time is current time
        cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_SIMPLEX,3,(255,0,255),3)
        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        

if __name__ == "__main__":  
    main()
                