import yolov5
import cv2

from Home.constant.config import ConfigWeb

model = yolov5.load(ConfigWeb.url_weight_yolo)
model.conf = ConfigWeb.yolo_conf
model.iou = ConfigWeb.yolo_iou


def detection(img, timeOut):
    # results = model(img, augment=True)
    results = model(img, ConfigWeb.yolo_size_img)
    # results.show()
    imgOut = results.render()[0]

    predictions = results.pred[0]
    scores = predictions[:, 4]

    if len(scores) > 0:
        if timeOut > 0:
            timeOut -= 1
        print(scores[0])
    else:
        if timeOut < ConfigWeb.time_out_alarm_max:
            timeOut += 1

    return imgOut, 0, timeOut
