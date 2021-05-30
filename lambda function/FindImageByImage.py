# import the necessary packages
import base64
import json
from io import BytesIO
import numpy as np
import time
import cv2
import os
import PIL
from PIL import Image
import boto3

s3 = boto3.resource('s3')
s3_client = boto3.client('s3')
# Get the service resource.
database = boto3.resource('dynamodb')

# construct the argument parse and parse the arguments
confthres = 0.3
nmsthres = 0.1

## Yolov3-tiny versrion
labelsPath = "coco.names"
cfgpath = "yolov3-tiny.cfg"
wpath = "yolov3-tiny.weights"


def get_labels(labels_path):
    # load the COCO class labels our YOLO model was trained on

    # print(yolo_path)
    # LABELS = open(lpath).read().strip().split("\n")
    with open("./yolo_tiny_configs/coco.names") as f:
        LABELS = f.read().strip().split("\n")
    return LABELS


def get_weights(weights_path):
    # derive the paths to the YOLO weights and model configuration
    bucket = "fit5225-layers-g30"
    key = weights_path

    respone = s3_client.get_object(Bucket=bucket, Key=key)
    weightsPath = respone['Body'].read()
    return weightsPath


def get_config(config_path):
    bucket = "fit5225-layers-g30"
    key = config_path

    respone = s3_client.get_object(Bucket=bucket, Key=key)
    configPath = respone['Body'].read()
    return configPath


def load_model(configpath, weightspath):
    # load our YOLO object detector trained on COCO dataset (80 classes)
    print("[INFO] loading YOLO from disk...")
    net = cv2.dnn.readNetFromDarknet(configpath, weightspath)
    return net


def do_prediction(image, net, LABELS):
    (H, W) = image.shape[:2]
    # determine only the *output* layer names that we need from YOLO
    ln = net.getLayerNames()
    ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    # construct a blob from the input image and then perform a forward
    # pass of the YOLO object detector, giving us our bounding boxes and
    # associated probabilities
    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416),
                                 swapRB=True, crop=False)
    net.setInput(blob)
    start = time.time()
    layerOutputs = net.forward(ln)
    # print(layerOutputs)
    end = time.time()

    # show timing information on YOLO
    print("[INFO] YOLO took {:.6f} seconds".format(end - start))

    # initialize our lists of detected bounding boxes, confidences, and
    # class IDs, respectively
    boxes = []
    confidences = []
    classIDs = []

    # loop over each of the layer outputs
    for output in layerOutputs:
        # loop over each of the detections
        for detection in output:
            # extract the class ID and confidence (i.e., probability) of
            # the current object detection
            scores = detection[5:]
            # print(scores)
            classID = np.argmax(scores)
            # print(classID)
            confidence = scores[classID]

            # filter out weak predictions by ensuring the detected
            # probability is greater than the minimum probability
            if confidence > confthres:
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
    idxs = cv2.dnn.NMSBoxes(boxes, confidences, confthres,
                            nmsthres)

    # ensure at least one detection exists
    # create an object list to collect the 'object' dictionary
    object = []

    if len(idxs) > 0:
        # loop over the indexes we are keeping
        for i in idxs.flatten():
            object.append(LABELS[classIDs[i]])

    return object


Lables = get_labels(labelsPath)
CFG = get_config(cfgpath)
Weights = get_weights(wpath)


def Start_detection(imagecode):
    try:

        im_bytes = base64.b64decode(imagecode)
        im_file = BytesIO(im_bytes)  # convert image to file-like object
        img = Image.open(im_file)  # img is now PIL Image object

        npimg = np.array(img)
        image = npimg.copy()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # load the neural net.  Should be local to this method as its multi-threaded endpoint
        nets = load_model(CFG, Weights)
        res = do_prediction(image, nets, Lables)

        return res

    except Exception as e:

        print("Exception  {}".format(e))


def lambda_handler(event, context):
    even = json.loads(event)
    imagecode = even['image']
    # imagecode = event['image']

    queryTags = Start_detection(imagecode)
    # print(queryTags)

    table = database.Table('LabelDetected')

    # response = table.query(
    #     KeyConditionExpression=Key('Tags').eq(queryTags)
    # )
    # return response['Items']

    response = table.scan()
    dbdata = response['Items']
    imageURL = []

    # Loop over the database items
    for index, element in enumerate(dbdata):

        url = element['URL']
        print(url)
        tags = element['Tags']
        imageInDatabase = set(tags)
        # print(imageInDatabase)
        # print(url)

        queryFromUser = set(queryTags)
        # print(queryFromUser)
        # print(queryTags)

        # If user's query match one image's JSON object, append this image to the list
        # If user's query input is an empty list, then ALL url in the database will be returned
        if queryFromUser == imageInDatabase:
            imageURL.append(url)

    result = {}
    if len(imageURL) > 0:
        result["links"] = imageURL
        jsonResult = json.dumps(result)
        return jsonResult
    else:
        return "There is no match images."

