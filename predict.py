# imports
import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from PIL import Image
matplotlib.pyplot.switch_backend('Agg')

def predict(image):
    """
        Logic for predicting class of image in this function
        Usage: from predict import predict
        params: pass the image which has to be predicted
        predict(img)
        """
    WEIGHT_PATH = os.path.join(os.getcwd(), 'YOLO/yolov3_final.weights')
    CFG_PATH = os.path.join(os.getcwd(), 'YOLO/yolov3_custom.cfg')
    net = cv2.dnn.readNet(WEIGHT_PATH, CFG_PATH)
    # initialize a list of colors to represent each possible class label
    np.random.seed(42)
    LABELS = [1, 2, 3, 4, 5, 6, 7, 8]
    COLORS = np.random.randint(0, 255, size=(3, 3), dtype="uint8")
    (H, W) = image.shape[:2]

    # determine only the "ouput" layers name which we need from YOLO
    ln = net.getLayerNames()
    ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    # construct a blob from the input image and then perform a forward pass of the YOLO object detector,
    # giving us our bounding boxes and associated probabilities
    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    layerOutputs = net.forward(ln)

    boxes = []
    confidences = []
    classIDs = []
    threshold = 0.2

    # loop over each of the layer outputs
    for output in layerOutputs:
        # loop over each of the detections
        for detection in output:
            # extract the class ID and confidence (i.e., probability) of
            # the current object detection
            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]

            # filter out weak predictions by ensuring the detected
            # probability is greater than the minimum probability
            # confidence type=float, default=0.5
            if confidence > threshold:
                # scale the bounding box coordinates back relative to the
                # size of the image, keeping in mind that YOLO actually
                # returns the center (x, y)-coordinates of the bounding
                # box followed by the boxes' width and height
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")

                # use the center (x, y)-coordinates to derive the top and
                # and left corner of the bounding box
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))

                # update our list of bounding box coordinates, confidences,
                # and class IDs
                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                classIDs.append(classID)

    # apply non-maxima suppression to suppress weak, overlapping bounding boxes
    idxs = cv2.dnn.NMSBoxes(boxes, confidences, threshold, 0.1)

    # ensure at least one detection exists
    if len(idxs) > 0:
        # loop over the indexes we are keeping
        for i in idxs.flatten():
            # extract the bounding box coordinates
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])

            # draw a bounding box rectangle and label on the image
            color = (255, 0, 0)
            cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
            text = "{}".format(LABELS[classIDs[i]], confidences[i])
            cv2.putText(image, text, (x + 15, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    print(classIDs)
    return image, classID

def display_img(img, cmap=None):
    print("in display image")
    fig = plt.figure(figsize=(12, 12))
    plt.axis(False)
    ax = fig.add_subplot(111)
    plt.imshow(img)
    plt.show()