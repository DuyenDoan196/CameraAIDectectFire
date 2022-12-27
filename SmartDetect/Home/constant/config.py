class ConfigWeb:
    base_root = '/Users/tmphuong/Desktop/Source/web/django/SmartDetect/'

    # DETECT CONFIG ===========
    url_weight_yolo = base_root + 'Home/data/weight/last.pt'
    url_root_detect_img = base_root + 'Home/media/detection/'
    time_out_alarm_max = 10
    # confidence threshold (0-1)
    yolo_conf = 0.3
    # NMS IoU threshold (0-1)
    yolo_iou = 0.5
    yolo_size_img = 1280
    # Firebase
    url_realtime_dtb = 'https://smartdetect-2b758-default-rtdb.firebaseio.com/'
    table_realtime_dtb = '/DetectFire'
    # MOCK ====================
    url_mock_webcam_1 = base_root + 'Home/data/mock/15.mp4'
    code_camA = 'camera_block_a'
    code_camB = 'camera_block_b'
    code_camC = 'camera_block_c'
    # If this is True using mock and or using webcam
    isMockWebcam = True
    area_code = "Khu A"