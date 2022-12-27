import os
from datetime import time

import cv2
from django.http import StreamingHttpResponse
from django.shortcuts import render
from django.views import View
from firebase import firebase
from Home import detect_webcam
from Home.constant.config import ConfigWeb
import datetime


# Create your views here.
class RenderHome(View):
    @staticmethod
    def get(request):
        return render(request, 'home/home.html')


def cameraA(request):
    return StreamingHttpResponse(stream(ConfigWeb.url_mock_webcam_1, ConfigWeb.code_camA), content_type='multipart/x-mixed-replace; boundary=frame')

def cameraB(request):
    return StreamingHttpResponse(stream(ConfigWeb.url_mock_webcam_2, ConfigWeb.code_camB), content_type='multipart/x-mixed-replace; boundary=frame')

def cameraC(request):
    return StreamingHttpResponse(stream(ConfigWeb.url_mock_webcam_3, ConfigWeb.code_camC), content_type='multipart/x-mixed-replace; boundary=frame')

def stream(webcam, code_cam):
    isVideo = ConfigWeb.isMockWebcam
    timeOut = ConfigWeb.time_out_alarm_max
    isWarningFire = False
    source = 0
    if isVideo:
        source = webcam
    cap = cv2.VideoCapture(source)
    urlDetect = ConfigWeb.url_root_detect_img + code_cam + ".jpg"

    while True:
        if not cap.isOpened() and isVideo:
            break
        ret, frame = cap.read()
        if not ret:
            print("Error: failed to capture image")
            break
        img, index, timeOut = detect_webcam.detection(frame, timeOut)
        # print(timeOut)
        if timeOut == 0 and not isWarningFire:
            isWarningFire = True
            # Send notify to device
            print("Detect fire =======>")
            SendWarningFire("Warning detect fire !!!", ConfigWeb.area_code)
        if timeOut == ConfigWeb.time_out_alarm_max:
            # reset status send notify detect fire
            isWarningFire = False
        cv2.imwrite(urlDetect, img)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + open(urlDetect, 'rb').read() + b'\r\n')


def SendWarningFire(message, area_code):
    # Firebase
    try:
        fb = firebase.FirebaseApplication(
            ConfigWeb.url_realtime_dtb, None)
        now = datetime.datetime.now()

        fb.post(ConfigWeb.table_realtime_dtb,
                {'id': str(now.timestamp()), 'message': message, 'area_code': area_code, 'time': str(now.day) + "-" + str(now.month) + "-"+ str(now.year) + " " + str(now.hour) + ":" + str(now.minute) })
    except ValueError:
        print(ValueError)
