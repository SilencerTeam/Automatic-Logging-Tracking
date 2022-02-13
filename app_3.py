import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import streamlit as st
from streamlit_lottie import st_lottie
import json
import requests
import csv 
import time
from pygame import mixer
mixer.init()

# from PIL import ImageGrab
def app():
    def load_lottieurl(url: str):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

    path = 'Room_3'
    images = []
    classNames = []
    myList = os.listdir(path)
    print(myList)
    for cl in myList:
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
    print(classNames)


    def findEncodings(images):
        encodeList = []

        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList


    def markAttendance(name):
        with open('Logged_ins.csv', 'r+') as f:
            myDataList = f.readlines()
            nameList = []
            for line in myDataList:
                entry = line.split(',')
                nameList.append(entry[0])
                if name not in nameList:
                    now = datetime.now()
                    dtString = now.strftime('%H:%M')                 
                    f.writelines(f'\n{name},{dtString},{"Meeting room"}')
            # time.sleep(1)

    def markNTA(name):
        with open('Warnings.csv', 'r+') as f:
            myDataList = f.readlines()
            nameList = []
            for line in myDataList:
                entry = line.split(',')
                nameList.append(entry[0])
                if name not in nameList:
                    now = datetime.now()
                    dtString = now.strftime('%H:%M')
                    f.writelines(f'\n{name},{dtString},{"Meeting room"}')
            # time.sleep(1)


    encodeListKnown = findEncodings(images)
    print('Encoding Complete')



    st.title("Meeting Room")
    lottie_img = load_lottieurl("https://assets7.lottiefiles.com/packages/lf20_fclga8fl.json")
    st_lottie(lottie_img,height=750, width=750)
    st.subheader("For video-capture mark the checkbox 'Run'")
    run = st.checkbox("Run")
    FRAME_WINDOW =st.image([])
    cap = cv2.VideoCapture(0)

    while run:
        success, img = cap.read()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                name = classNames[matchIndex].upper()
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                markAttendance(name)
            else:
                name = "Not_allowed"
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1,y1), (x2, y2), (0, 0, 255), 2)
                cv2.putText(img, "Not Allowed", (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                mixer.music.load('alarm.mp3')
                mixer.music.play()
                markNTA(name)
                


        cv2.imshow('Webcam_3', img)
        FRAME_WINDOW.image(img)

        k = cv2.waitKey(6) & 0xFF
        if k == 27:
            cv2.destroyAllWindows()
            break
