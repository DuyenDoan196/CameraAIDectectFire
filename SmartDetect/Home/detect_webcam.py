# YOLO object detection
import cv2 as cv
import numpy as np
import time
coco = '/Users/tmphuong/Desktop/Source/web/django/SmartDetect/Home/data/yolo/model.names'
cfg = '/Users/tmphuong/Desktop/Source/web/django/SmartDetect/Home/data/yolo/yolov3_custom.cfg'
# weight = '/Users/tmphuong/Desktop/Source/web/django/SmartDetect/Home/data/yolo/yolo_detect_fire.weights'
weight = '/Users/tmphuong/Desktop/Source/web/django/SmartDetect/Home/data/yolo/yolov3_custom1_1000.weights'
#Webcam
def detection(img):
        value = 416
        # Tải lên danh sách Label và random matrix màu
        classes = ''
        if "\n" in (open(coco).read()):
            classes = open(coco).read().strip().split('\n')
        else:
            classes = open(coco).read()
        np.random.seed(10)
        colors = np.random.randint(0, 255, size=(122, 3), dtype='uint8')
        # Khởi tạo và tải yolo lên mạng neuron
        net = cv.dnn.readNetFromDarknet(cfg, weight)
        net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
        net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)

        # Xác định đầu ra
        ln = net.getLayerNames()
        ln = [ln[i - 1] for i in net.getUnconnectedOutLayers()]
        # Tạo 1 đốm màu từ hình ảnh
        # blobFromImage(Nguồn hình,tỉ lệ,kích thước,đổi RGB->BGR,ko cắt ảnh
        blob = cv.dnn.blobFromImage(img, 1/255.0, (value, value), swapRB=True, crop=False)

        net.setInput(blob)
        outputs = net.forward(ln)
        boxes = []
        confidences = []
        classIDs = []
        h, w = img.shape[:2]
        for output in outputs:
            for detection in output:
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]
                print(confidence)
                if confidence > 0:
                    box = detection[0:4] * np.array([w, h, w, h])
                    (centerX, centerY, width, height) = box.astype("int")
                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))
                    box = [x, y, int(width), int(height)]
                    boxes.append(box)
                    confidences.append(float(confidence))
                    classIDs.append(classID)
        #Lấy ra vị trí có chỉ số nhận dạng lớn nhất
        indexMax = -1
        # print(confidences)
        if len(confidences) > 0.98:
            indexMax = np.argmax(confidences)
        indices = cv.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        if len(indices) > 0:
            # for i in indices.flatten():
            if(indexMax != -1):
                print(str(indexMax)+' '+classes[classIDs[indexMax]])
                (x, y, w, h) = (boxes[indexMax][0], boxes[indexMax][1], boxes[indexMax][2], boxes[indexMax][3])
                color = [int(c) for c in colors[classIDs[indexMax]]]
                cv.rectangle(img, (x, y), (x + w, y + h), color, 2)
                text = "{}: {:.4f}".format(classes[classIDs[indexMax]], confidences[indexMax]*100)
                cv.putText(img, text, (x, y - 5), cv.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                return img, indexMax, classIDs[indexMax], confidences[np.argmax(confidences)]
        return img, indexMax, -1, -1