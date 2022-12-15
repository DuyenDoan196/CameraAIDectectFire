import os
from datetime import time

import cv2
from django.http import StreamingHttpResponse
from django.shortcuts import render
from django.views import View

from Home import detect_webcam


# Create your views here.
class RenderHome(View):
    def get(self, request):
        return render(request, 'home/home.html')

def camera(request):
    return StreamingHttpResponse(stream(), content_type='multipart/x-mixed-replace; boundary=frame')

def stream():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: failed to capture image")
            break
        urlImgWebcam = '/Users/tmphuong/Desktop/Source/web/django/SmartDetect/Home/media/documents/webcam.jpg'
        try:
            os.remove(urlImgWebcam)
        except:
            pass
        cv2.imwrite(urlImgWebcam, frame)
        img, index, _, _ = detect_webcam.detection(frame)
        if index != -1:
            urlDetect = "/Users/tmphuong/Desktop/Source/web/django/SmartDetect/Home/media/detection/webcam.jpg"
            cv2.imwrite(urlDetect, img)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + open(urlDetect, 'rb').read() + b'\r\n')

       # # temp = loader.get_template('Contact/webcam.html')
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + open(urlImgWebcam, 'rb').read() + b'\r\n')