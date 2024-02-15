import asyncio
import cv2
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import os
from dotenv import load_dotenv
from imutils import face_utils
import matplotlib.pyplot as plt
import numpy as np
import argparse
import imutils
import dlib 
import face_recognition
from datetime import datetime, timedelta
import subprocess


load_dotenv()

async def main():

    #Confirm Face-recongnition
    detector = dlib.get_frontal_face_detector()
    predictor = face_recognition.api.pose_predictor_68_point
    print("setting model")

    # Capture video from the default camera
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 512)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 512)
    # Set capture frame rate
    cap.set(cv2.CAP_PROP_FPS, 60)
    print("Ready to capture")

    frame_count = 0
    executor = ThreadPoolExecutor(max_workers=10)
    last_sent_time = datetime.now() - timedelta(seconds=2)
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            image = frame
            image = imutils.resize(image, width=500) 
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
            rects = detector(gray, 1)

            classfication = {} # using to classfication to face configure

            for (i, rect) in enumerate(rects):
                shape = predictor(gray, rect)
                shape = face_utils.shape_to_np(shape)
                (x, y, w, h) = face_utils.rect_to_bb(rect)
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(image, "Face #{}".format(i + 1), (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                
                for (i, (x, y)) in enumerate(shape):
                    cv2.circle(image, (x, y), 1, (0, 255, 255), -1)
                    classfication[x]=y

            # easy vtuber를 위한 offset 
            result = {k: v for k, v in classfication.items() if (247 <= k <= 264 and 168 <= v <= 178) or(222 <= k <= 242 and 139 <= v <= 153)}
            
            c_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            cv2.imwrite('output_image.jpg', frame) ##############################
            # face confiugure가 성공적일 경우
            if len(result) != 0:
                current_time = datetime.now()
                if current_time - last_sent_time >= timedelta(seconds=0.1):
                    print("shot CCTV.SD")
                    #####################################
                    subprocess.run(["python", "pub_openark.py", "output_image.jpg", "--function_name", "cctv.sd"])
                    #####################################
                    last_sent_time = current_time
            # 기본적으로 보내는 곳
            subprocess.run(["python", "pub_openark.py", "output_image.jpg", "--function_name", "cctv.default"]) ##############################
            frame_count += 1
            # Adjust sleep time if necessary for your specific hardware
            # if (frame_count%20) == 0 : print(filename); os.system(f'rm -rf *.jpg')
            await asyncio.sleep(1/60)
    finally:
        cap.release()
        cv2.destroyAllWindows()
        await nc.close()
        executor.shutdown(wait=True)

if __name__ == '__main__':
    asyncio.run(main())
