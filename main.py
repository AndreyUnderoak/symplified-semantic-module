from ultralytics import YOLO
import cv2
import math
import sys 
from termcolor import colored
from classes.Topic_reader import Topic_reader, TopicException
from classes.SemanticObject import SemanticObject
from classes.Transmitter import Transmitter as Sender

from numpy import array as nparray

def flatten(xss):
    return [x for xs in xss for x in xs]

if(len(sys.argv) < 2):
    print(colored("Please write topic: python3 dataset_maker <files_name> <geo_topic> <image_topic> <auto/none>",'red'))
    exit()
img_topic = sys.argv[1]
topic_reader = Topic_reader(img_topic)

max_pairs = 10

#UDP Sender init
sender = Sender("localhost", 8080, max_pairs)

# message = [1000,1000, 388, 2103,1080,1920]
# sender.send(message)
# sender.send(str.encode("localhost"))

# print(bytes(message))

cv2.namedWindow("Display", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Display", 640, 640)

# model
model = YOLO("yolo-Weights/yolov8n.pt")

# object classes
classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
              "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
              "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
              "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
              "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
              "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush"
              ]


while True:
    try:
        img = topic_reader.get_latest_image()
        results = model(img, stream=True)
    except TopicException as e:
        # print(colored(e.message,'red'))
        continue

    message = []
    num = 0
    # coordinates
    for r in results:
        boxes = r.boxes

        for box in boxes:
            # bounding box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values

            xcell = x1+int((x2-x1)/2)
            ycell = y1+int((y2-y1)/2)

            # print(x1, y1, x2, y2)

            cv2.circle(img, (xcell, ycell), radius=1, color=(0, 0, 255), thickness=2)
            # put box in cam
            # cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

            # # confidence
            # confidence = math.ceil((box.conf[0]*100))/100
            # print("Confidence --->",confidence)

            # class name
            cls = int(box.cls[0])
            
            #can be chair
            if((classNames[cls]=="bottle") and  num < max_pairs):
                num+=1
                message.append(SemanticObject(xcell,ycell, object_id=cls))
                
                # print(message)
                print("Class name -->", classNames[cls])
                print("Coors --> ", xcell, " ", ycell)

            # object details
            org = [x1, y1]
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 1
            color = (255, 0, 0)
            thickness = 2

            cv2.putText(img, classNames[cls], org, font, fontScale, color, thickness)

        print("Sending:")
        l = []
        for m in message:
            l.append(m.to_list())

        print(flatten(l))

        sender.send(flatten(l))

    cv2.imshow('Display', img)
    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()
