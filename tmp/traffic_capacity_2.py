import logging
import logging.handlers
import os
import time
import sys
import cv2
import numpy as np
import utils
import matplotlib.pyplot as plt
import time
import threading
from firebase_server_connect import FirebaseManager

cv2.ocl.setUseOpenCL(False)

# ============================================================================
from pipeline_2 import (
    PipelineRunner,
    CapacityCounter
)
# ============================================================================
SHAPE = (720, 1280)
base = np.zeros(SHAPE + (3,), dtype=np.uint8)
log = utils.init_logging()
fm = FirebaseManager()

# ============================================================================

def _level(capac):
    capac *= 100
    if capac >= 0 and capac <= 40:
        return 3
    elif capac > 40 and capac <= 60:
        return 2
    elif capac > 60 and capac <= 80:
        return 1
    else:
        return 0

def runCamera(input_video, camera_name="Undefined", AREA_PTS=np.array([[0, 610], [570, 260], [630, 260], [525, 700]]), save_image=False, image_dir="./"):
    if save_image and not os.path.exists(image_dir):
        os.makedirs(image_dir)
    area_mask = cv2.fillPoly(base, [AREA_PTS], (255, 255, 255))[:, :, 0]
    capacity_counter = CapacityCounter(area_mask=area_mask, save_image=save_image, image_dir=image_dir)
    pipeline = PipelineRunner(pipeline=[capacity_counter], log_level=logging.DEBUG)
    cap = cv2.VideoCapture("stream videos/road1.mp4")
    frame_number = 0

    CURRENT_COUNTER = [time.time()] * 3
    LEVEL_COUNT = np.zeros(4)
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                log.error("Capture failed, please try again!...")
                return
            else:
                frame_number += 1
                pipeline.set_context({'frame': frame, 'frame_number': frame_number})
                context = pipeline.run()
                #cv2.imshow("map", context['t'])
                cv2.putText(context['base_frame'], str(context['capacity']), (10,500), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.imshow("base_frame", context['base_frame'])
                # print(context['capacity'])
                # print(frame_number)
                if cv2.waitKey(33) == 27:
                    break

    except Exception as e:
        log.exception(e)