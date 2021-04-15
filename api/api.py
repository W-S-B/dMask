from flask import Flask, render_template, Response
import json

from datetime import datetime
from dMask import db, bcrypt
from dMask.models import User, Status

import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile

from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image


from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

import cv2
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()

cap = cv2.VideoCapture(0)  

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)

cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

MODEL_NAME = 'object_detection/new_graph' 

PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'

PATH_TO_LABELS = os.path.join('object_detection/data', 'label_map.pbtxt')

NUM_CLASSES = 3

classes = ['Mask', 'WrongMask', 'NoMask']

detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

def matches(List):
    return max(set(List), key=List.count)

app = Flask(__name__)

@app.route('/api', methods=['GET'])
def api():
    return{
        'video': 'https://www.6connex.com/wp-content/uploads/virtual_events_and_environments_03.jpg'
    }

def gen():
    entries = []
    begin_time = 81
    Mask = 0, NoMask = 0, WrongMask = 0

    with detection_graph.as_default():
        with tf.Session(graph=detection_graph) as sess:
            while True:
                d = datetime.now()
                t = d.time()
                if t.hour > 6 and t.hour < 22:
                    ret, image_np = cap.read()
                    image_np_expanded = np.expand_dims(image_np, axis=0)
                    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
                    boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
                    scores = detection_graph.get_tensor_by_name('detection_scores:0')
                    classes = detection_graph.get_tensor_by_name('detection_classes:0')
                    num_detections = detection_graph.get_tensor_by_name('num_detections:0')
                    (boxes, scores, classes, num_detections) = sess.run(
                        [boxes, scores, classes, num_detections],
                        feed_dict={image_tensor: image_np_expanded})

                    if begin_time < 10:    
                        for i in range(min(1, np.squeeze(boxes).shape[0])):
                            if np.squeeze(classes)[i] in category_index.keys():
                                class_name = category_index[np.squeeze(classes)[i]]['name']
                            if np.squeeze(scores)[i] > 0.7:    
                                if class_name:
                                    display_str = str(class_name)
                                    entries.append(display_str)
                        begin_time += 1
                    elif begin_time == 10:
                        if matches(entries) == "NoMask":
                            print("Put your Mask ON")
                            NoMask += 1
                        elif matches(entries) == "WrongMask":
                            print("Fix Your Mask with the instructions below")
                            WrongMask += 1
                        elif matches(entries) == "Mask":
                            print("You may pass")
                            Mask += 1
                        begin_time += 1
                    else:
                        for i in range(min(1, np.squeeze(boxes).shape[0])):
                            if np.squeeze(classes)[i] in category_index.keys():
                                class_name = category_index[np.squeeze(classes)[i]]['name']
                            if np.squeeze(scores)[i] > 0.7:    
                                if class_name:
                                    begin_time = 0
                                    del entries[:]
                                    display_str = str(class_name)
                                    entries.append(display_str)

                    vis_util.visualize_boxes_and_labels_on_image_array(
                        image_np,
                        np.squeeze(boxes),
                        np.squeeze(classes).astype(np.int32),
                        np.squeeze(scores),
                        category_index,
                        use_normalized_coordinates=True,
                        line_thickness=6,
                        min_score_thresh=.7,
                        max_boxes_to_draw=1)
                    ret, jpeg = cv2.imencode('.jpg', cv2.resize(image_np, (640, 480)))
                    frame = jpeg.tobytes()
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
                elif t.hour == 0 and t.minute == 0 and t.second == 0:
                    status = Status(masks_count=10, passed_people=Mask+WrongMask+NoMask, passed_green=Mask, passed_yellow=WrongMask, passed_red=NoMask)
                    db.session.add(status)
                    db.session.commit()


@app.route("/history")
def history():
    with open("messages.json", "r") as f:
        data = json.load(f)
    return data

@app.route('/video_feed')
def video_feed():

    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')