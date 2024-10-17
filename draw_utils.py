import cv2

def draw_boxes(img, boxes, class_ids, confidences, classes, tracked_objects, cars):
    for (box, class_id, confidence) in zip(boxes, class_ids, confidences):# draw bouncing boxs
        x, y, w, h = box
        color = (0, 255, 0)
        cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
        label = f"{classes[class_id]} {confidence:.2f}"
        cv2.putText(img, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    for (object_id, centroid) in tracked_objects.items():# draw ids
        text = f"ID {object_id}"
        cv2.putText(img, text, (centroid[0] - 10, centroid[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        cv2.circle(img, (centroid[0], centroid[1]), 4, (255, 0, 0), -1)
    # draw line count
    yl = int(img.shape[0] / 2)
    xl = int(img.shape[1])
    cv2.line(img, (0, yl), (xl, yl), (250, 100, 100), 2)
    # numb cars
    num = f"{cars}"
    cv2.rectangle(img, (0, 0), (100, 50), (255, 30, 250))
    cv2.putText(img, num, (50, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
