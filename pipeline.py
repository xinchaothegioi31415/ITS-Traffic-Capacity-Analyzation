import os
import logging

import numpy as np
import cv2
import matplotlib.pyplot as plt
import utils


AREA_COLOR = (66, 183, 42)


class PipelineRunner(object):
    def __init__(self, pipeline=None, log_level=logging.DEBUG):
        self.pipeline = pipeline or []
        self.context = {}
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(log_level)
        self.log_level = log_level
        self.set_log_level()

    def set_context(self, data):
        self.context = data

    def add(self, processor):
        if not isinstance(processor, PipelineProcessor):
            raise Exception(
                'Processor should be an isinstance of PipelineProcessor.')
        processor.log.setLevel(self.log_level)
        self.pipeline.append(processor)

    def remove(self, name):
        for i, p in enumerate(self.pipeline):
            if p.__class__.__name__ == name:
                del self.pipeline[i]
                return True
        return False

    def set_log_level(self):
        for p in self.pipeline:
            p.log.setLevel(self.log_level)

    def run(self):
        for p in self.pipeline:
            self.context = p(self.context)

        return self.context


class PipelineProcessor(object):
    '''
        Base class for processors.
    '''

    def __init__(self):
        self.log = logging.getLogger(self.__class__.__name__)
        

class CapacityCounter(PipelineProcessor):

    def __init__(self, area_mask, save_image=False, image_dir='./'):
        super(CapacityCounter, self).__init__()
    
        self.area_mask = area_mask
        self.all = np.count_nonzero(area_mask)
        self.image_dir = image_dir
        self.save_image = save_image
        
    def calculate_capacity(self, frame, frame_number):
        base_frame = frame
        # CLAHE (Contrast Limited Adaptive Histogram Equalization)
        # this used for noise reduction at night time
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        cl1 = clahe.apply(frame)
    
        edges = cv2.Canny(frame,50,70)
        edges = ~edges
        blur = cv2.bilateralFilter(cv2.blur(edges,(21,21), 100),9,200,200)
        _, threshold = cv2.threshold(blur,230, 255,cv2.THRESH_BINARY)
        
        t = cv2.bitwise_and(threshold,threshold,mask = self.area_mask)
        
        free = np.count_nonzero(t)
        capacity = 1 - float(free)/self.all

        if self.save_image:
            img = np.zeros(base_frame.shape, base_frame.dtype)
            img[:, :] = AREA_COLOR
            mask = cv2.bitwise_and(img, img, mask=self.area_mask)
            cv2.addWeighted(mask, 1, base_frame, 1, 0, base_frame)
            cv2.imshow("base", base_frame)
            fig = plt.figure()
            fig.suptitle("Capacity: {}%".format(capacity*100), fontsize=16)
            plt.subplot(211),plt.imshow(base_frame),plt.title('Original')
            plt.xticks([]), plt.yticks([])
            plt.subplot(212),plt.imshow(t),plt.title('Capacity map')
            plt.xticks([]), plt.yticks([])

            fig.savefig(self.image_dir + ("/processed_%s.png" % frame_number), dpi=500)
            plt.close()
            
        return capacity
        
    def __call__(self, context):
        frame = context['frame'].copy()
        frame_number = context['frame_number']
        
        capacity = self.calculate_capacity(frame, frame_number)

        context['capacity'] = capacity
        
        return context