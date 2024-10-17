import cv2
import numpy as np

YOLOV3_CFG = 'yolov4-tiny.cfg'
YOLOV3_WEIGHT = 'yolov4-tiny.weights'
CLASS_NAMES_FILE = 'coco.names'

CONFIDENCE_SETTING = 0.4
NMS_THRESHOLD = 0.2
YOLOV3_WIDTH = 416
YOLOV3_HEIGHT = 416

def get_output_layers(net):
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers().flatten()]
    return output_layers

def load_class_names(file_path):
    with open(file_path, 'r') as f:
        classes = f.read().strip().split('\n')
    return classes

def detect_objects(net, image):
    height, width = image.shape[:2]
    blob = cv2.dnn.blobFromImage(image, 0.00392, (YOLOV3_WIDTH, YOLOV3_HEIGHT), swapRB=True, crop=False)
    net.setInput(blob)
    
    layer_outputs = net.forward(get_output_layers(net))
    boxes, confidences, class_ids = [], [], []
    vehicle_class_ids = [2, 3, 5, 7]

    for out in layer_outputs:
        for detection in out:
            scores = detection[5:]
            confidence = max(scores)
            class_id = np.argmax(scores)
            if confidence > CONFIDENCE_SETTING and class_id in vehicle_class_ids:
                center_x, center_y, w, h = (detection[0:4] * np.array([width, height, width, height])).astype(int)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(int(class_id))

    indices = cv2.dnn.NMSBoxes(boxes, confidences, CONFIDENCE_SETTING, NMS_THRESHOLD)
    filtered_boxes, filtered_confidences, filtered_class_ids = [], [], []
    if len(indices) > 0:
        for i in indices.flatten():
            filtered_boxes.append(boxes[i])
            filtered_class_ids.append(class_ids[i])
            filtered_confidences.append(confidences[i])

    return filtered_boxes, filtered_confidences, filtered_class_ids
