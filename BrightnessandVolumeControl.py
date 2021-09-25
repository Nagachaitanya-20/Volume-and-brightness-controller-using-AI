import cv2
import mediapipe
import numpy as np
import time
import HandDectectorModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import screen_brightness_control as sbc
all_screens_brightness = sbc.get_brightness()
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange=volume.GetVolumeRange()

minvol=volRange[0]
maxvol=volRange[1]
volBar,vol,volper=400,0,0
briBar,vol,briper=400,0,0
detector=htm.handDectector(detectionCon=0.7,maxHands=1)
wCam,hCam=1080,960
cap=cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
pTime=0
cTime=0
area=0
colorVol=(255,0,0)
while True:
    success,img= cap.read()

    #Find Hand
    img=detector.findHands(img)
    lmList,bbox=detector.findPosition(img,draw=True)
    if len(lmList)!=0:
        wB=bbox[2]-bbox[0]
        hB=bbox[3]-bbox[1]
        area=(wB*hB)//100
        #print(area//100)
        if area>750:
            cv2.putText(img,"Hey !! ready to set Volume ",(700,600),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),3)
            

            #Filter based on size

            #Find distance between index and thumb
            length,img,lineinfo=detector.findDistance(4,8,img)
            #print(length)

            #convert Volume
            volBar=np.interp(length,[50,200],[400,150])
            volper=np.interp(length,[50,200],[0,100])

            #print(vol)
            smoothness=10
            volper=smoothness*round(volper/smoothness)
            fingers=detector.fingersUp()
            #print(fingers)
            #volume.SetMasterVolumeLevel(vol, None)
            if not fingers[4]:
                volume.SetMasterVolumeLevelScalar(volper/100,None)
                cv2.circle(img,(lineinfo[4],lineinfo[5]),15,(0,255,0),cv2.FILLED)
                colorVol=(0,255,0)
            else:
                colorVol=(255,0,0)

        else:
            cv2.putText(img,"Hey!! ready to set Brightness",(700,600),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),3)#50,400

            #Filter based on size

            #Find distance between index and thumb
            length,img,lineinfo=detector.findDistance(4,8,img)
            #print(length)

            #convert Brightness
            briBar=np.interp(length,[50,180],[400,150])
            briper=np.interp(length,[50,180],[0,100])

            
            smoothness=10
            briper=smoothness*round(briper/smoothness)
            fingers=detector.fingersUp()
            #print(fingers)
            if not fingers[4]:
                sbc.set_brightness(int(briper))
                cv2.circle(img,(lineinfo[4],lineinfo[5]),15,(0,255,0),cv2.FILLED)
                colorVol=(0,255,0)
            else:
                colorVol=(255,0,0)
    if area>750:
        cv2.rectangle(img,(50,150),(85,400),(0,255,0),3)
        cv2.rectangle(img,(50,int(volBar)),(85,400),(0,255,0),cv2.FILLED)
        cv2.putText(img,f'{int(volper)}',(40,450),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),3)
        cVol=int(volume.GetMasterVolumeLevelScalar()*100)
        cv2.putText(img,f'vol set:{int(cVol)}',(750,50),cv2.FONT_HERSHEY_COMPLEX,1,colorVol,3)
        cTime=time.time()
        fps=1/(cTime-pTime)
        pTime=cTime
        cv2.putText(img,f'FPS:{int(fps)}',(40,50),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),3)
        cv2.imshow("IMG",img)
        cv2.waitKey(1)
    else :
        cv2.rectangle(img,(50,150),(85,400),(0,255,0),3)
        cv2.rectangle(img,(50,int(briBar)),(85,400),(0,255,0),cv2.FILLED)
        cv2.putText(img,f'{int(briper)}',(40,450),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),3)
        cbri=int(sbc.get_brightness(display=0))
        cv2.putText(img,f'Brightness set:{int(cbri)}',(750,50),cv2.FONT_HERSHEY_COMPLEX,1,colorVol,3)
        cTime=time.time()
        fps=1/(cTime-pTime)
        pTime=cTime

        cv2.putText(img,f'FPS:{int(fps)}',(40,50),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),3)
        cv2.imshow("IMG",img)
        cv2.waitKey(1)



















        #chnage(640,480)