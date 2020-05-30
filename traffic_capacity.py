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
from pipeline import (
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
    cap = cv2.VideoCapture(input_video)
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
                #cv2.imshow(camera_name, frame)
                if time.time() - CURRENT_COUNTER[1] >= 3:
                    CURRENT_COUNTER[1] = time.time()
                    pipeline.set_context({'frame': frame, 'frame_number': frame_number})
                    #fm.update_current_time_video(camera_name, "video_position", int(cap.get(cv2.CAP_PROP_POS_MSEC)))
                    context = pipeline.run()
                    if time.time() - CURRENT_COUNTER[0] >= 15:
                        fm.update_capacity(parent_camera=camera_name,capacity_value=context['capacity'])
                        fm.update_level(camera_name, "capacity_level", _level(context['capacity']))
                        fm.update_time()
                        currTime = time.time()
                    if time.time() - CURRENT_COUNTER[2] < 300:
                        LEVEL_COUNT[_level(context['capacity'])] += 1
                    else:
                        fm.update_level(camera_name, "level", int(LEVEL_COUNT.argmax()))
                        CURRENT_COUNTER[2] = time.time()
                        LEVEL_COUNT = np.zeros(4)
                if cv2.waitKey(33) == 27:
                    break

    except Exception as e:
        log.exception(e)