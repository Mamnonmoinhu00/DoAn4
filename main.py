import cv2
import time
from datetime import datetime
import threading
from picamera2 import Picamera2
from yolo_utils import detect_objects, load_class_names
from tracking_utils import CentroidTracker
from draw_utils import draw_boxes
from firebase import add_location
from gps import get_gps_coordinates
from prediction import predict_traffic_condition

# Các biến -----------------------------------------------------------------------------------
cars = 0
re_count = 0
def update_data():
    global cars, re_count
    # GPS -----------------------------------------------------------------------------------
    # lat, long = get_gps_coordinates()
    long, lat = 105.849, 21.0285
    while True:
        hour_now = datetime.now().hour
        print(cars)
        result = predict_traffic_condition(long, lat, hour_now, cars)
        #result = 1
        location_name = 'location4'  # Tên của location
        # sent data to firebase
        add_location(location_name, result, lat, long)
        # reset lưu lượng: cars
        re_count = 1
        # Đợi 1 giờ trước khi cập nhật lại
        time.sleep(10)

# Chạy hàm cập nhật trong một luồng riêng biệt
thread = threading.Thread(target=update_data)
thread.start()

#-----------------------------------------------------------------------------------
def object_detection():
    net = cv2.dnn.readNetFromDarknet('yolov4-tiny.cfg', 'yolov4-tiny.weights')
    classes = load_class_names('coco.names')

    tracker = CentroidTracker()
    picam2 = Picamera2()
    picam2.start()
    #----------------------------
    global cars,re_count
    
    while True:
        frame = picam2.capture_array()
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        
        boxes, confidences, class_ids = detect_objects(net, frame)
        tracked_objects, cars = tracker.update(boxes)
        draw_boxes(frame, boxes, class_ids, confidences, classes, tracked_objects, cars)
        
        if(re_count):
            for v in tracker.id_counted:
                print('l',v,'l')
            tracker.reset_parameters()
            re_count = 0
        cv2.imshow("Object Detection and Tracking", frame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
    picam2.close()

if __name__ == '__main__':
    object_detection()
