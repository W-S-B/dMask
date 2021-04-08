import tensorflow as tf
from object_detection.utils import config_util
from object_detection.protos import pipeline_pb2
from google.protobuf import text_format

import os
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils
from object_detection.builders import model_builder

import six
import cv2
import numpy as np
import time

WORKSPACE_PATH = 'Tensorflow/workspace'
SCRIPTS_PATH = 'Tensorflow/scripts'
APIMODEL_PATH = 'Tensorflow/models'
ANNOTATION_PATH = WORKSPACE_PATH + '/annotations'
IMAGE_PATH = WORKSPACE_PATH + '/images'
MODEL_PATH = WORKSPACE_PATH + '/models'
PRETRAINED_MODEL_PATH = WORKSPACE_PATH + '/pre-trained-models'
CONFIG_PATH = MODEL_PATH + '/my_ssd_mobnet/pipeline.config'
CHECKPOINT_PATH = MODEL_PATH + '/my_ssd_mobnet/'
CUSTOM_MODEL_NAME = 'my_ssd_mobnet'
CONFIG_PATH = MODEL_PATH +'/' +CUSTOM_MODEL_NAME +'/pipeline.config'

labels = [{'name':'Mask', 'id':1}, {'name':'NoMask', 'id':2}, {'name':'WrongMask', 'id':3}]
classes = ['Mask', 'WrongMask', 'NoMask']

def matches(List):
    return max(set(List), key=List.count)

configs = config_util.get_configs_from_pipeline_file(CONFIG_PATH)
detection_model = model_builder.build(model_config=configs['model'], is_training=False)

ckpt = tf.compat.v2.train.Checkpoint(model=detection_model)
ckpt.restore(os.path.join(CHECKPOINT_PATH, 'ckpt-31')).expect_partial()

@tf.function
def detect_fn(image):
    image, shapes = detection_model.preprocess(image)
    prediction_dict = detection_model.predict(image, shapes)
    detections = detection_model.postprocess(prediction_dict, shapes)
    return detections


category_index = label_map_util.create_category_index_from_labelmap(ANNOTATION_PATH +'/label_map.pbtxt')

cap = cv2.VideoCapture(0)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
def Run_Cam():
    begin_time = 0
    entries = []

    while begin_time < 60:
        ret, frame = cap.read()
        image_np = np.array(frame)
    
        input_tensor = tf.convert_to_tensor(np.expand_dims(image_np, 0), dtype=tf.float32)
        detections = detect_fn(input_tensor)

        num_detections = int(detections.pop('num_detections'))
        
        detections = {key:value[0, :num_detections].numpy() for key,value in detections.items()}
        detections['num_detections'] = num_detections
        detections['detection_classes'] = detections['detection_classes'].astype(np.int64) 
        label_id_offset = 1
        image_np_with_detections = image_np.copy()

        for i in range(min(1, detections['detection_boxes'].shape[0])):
            if detections['detection_classes'][i]+1 in category_index.keys():
                class_name = category_index[detections['detection_classes'][i]+1]['name']
            display_str = str(class_name)
            if detections['detection_scores'][i] > 0.3:
                if not display_str:
                    display_str = '{}%'.format(round(100*detections['detection_scores'][i]))
                else:
                    display_str = '{}: {}%'.format(display_str, round(100*detections['detection_scores'][i]))
                    entries.append(class_name)

        viz_utils.visualize_boxes_and_labels_on_image_array(
            image_np_with_detections,
            detections['detection_boxes'],
            detections['detection_classes']+label_id_offset,
            detections['detection_scores'],
            category_index,
            use_normalized_coordinates = True,
            max_boxes_to_draw = 1,
            min_score_thresh = 0.3,
            agnostic_mode = False
        )

        cv2.imshow('object detection', cv2.resize(image_np_with_detections, (800, 600)))


        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            break
        begin_time += 1
    print(matches(entries))
while True:
    input("Press Enter to continue...")
    Run_Cam()
