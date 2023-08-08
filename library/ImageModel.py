import os
from PIL import Image
import numpy as np
import cvlib
import cv2
from .util import _quantify_image, _find_image_centroid,_cosine_similarity 

class ImageCounter():
    def __init__(self, filename):
        self.labels = ['apple']
        self.filename = filename
        self.image_array = np.asarray(Image.open(filename))
        # self.image_array = np.asarray(Image.open(filename).resize((512,512),2))
        self.cropped_image = []
        self.bboxes = []
        self.count = -1
        self.cropped_masked_image = []
        self.color_analyzer = []

    def count_object(self):
        box, label, count = self._detect_object()
        self.count = 0
        for b, l, c in zip(box, label, count):
            if l in self.labels and c > 0.5:
                self.count += 1
                self.bboxes.append(b)
        if self.count > 0:
            self.crop_image()
            return self.count
        else: 
            return False

    def _detect_object(self):
        # We are using the yolov3 as the base detectron
        box, label, count = cvlib.detect_common_objects(self.image_array,model='yolov3') 
        return box, label, count

    def crop_image(self):
        self.cropped_image = []
        for box in self.bboxes:
            cropped_image = self.image_array[box[1]:box[3],box[0]:box[2]] #crop the image based on bounding boxes
            self.cropped_image.append(cropped_image)
            self.cropped_masked_image.append(self._circular_crop(cropped_image)) #crop the image based on the circular mask
        return self.cropped_image, self.cropped_masked_image

    def _circular_crop(self, image):
        # as apple is very likely circular we will crop it to be circle
        image = image.copy()
        r = int(min(image.shape[:2])/2) # radius
        if r == 0:
            raise Exception('ERROR zRadius 0')
        mask = np.full((image.shape[0], image.shape[1]), 0, dtype=np.uint8) # create a mask
        mask = cv2.circle(mask.copy() ,(r,r), r, (255,255,255),-1)# create circle mask, center, radius, fill color, size of the border
        fg = cv2.bitwise_or(image, image, mask=mask) # get only the inside pixels
        return fg, mask

    def create_color_files(self):
        temp_ca = None
        for idx, (cmi_image,cmi_mask) in enumerate(self.cropped_masked_image):
            temp_ca = ColorAnalyzer(cmi_image, cmi_mask)
            temp_ca.operate(idx+1)
            self.color_analyzer.append(temp_ca)
        return temp_ca

class ColorAnalyzer():
    def __init__(self, imageArray, imageMask):
        self.src = imageArray           # Reads in image source
        self.mask = imageMask           # Mask for weighting
        # Empty dictionary container to hold the colour frequencies
        self.color_labels = ['red','green','yellow', 'black']
        self.color_threshold ={'red':[255,10,10],'green':[10,255,10],'yellow':[150,150,0], 'black':[1,1,1]}
        self.color_label = None

    def operate(self, image_count): #rapper to do all the operation
        self.count_colors()
        self.save_image(image_count)

    def count_colors(self):
        quantized_image = _quantify_image(self.src)
        centroid, count =_find_image_centroid(quantized_image)
        similarities = {}
        for cen,cou in zip(centroid,count):
            # temp = {}
            for cl in self.color_labels:
                similarities[cl] = cou * _cosine_similarity(np.array(cen), np.array(self.color_threshold[cl]))
                # print(cl, self.color_threshold[cl], cen, similarities[cl])
        index = sorted(similarities,key=similarities.__getitem__, reverse=True)
        if index[0] == 'black':
            self.color_label=index[1]
        else:
            self.color_label=index[0]
        return index, similarities       

    def save_image(self, count, base_folder='./Image/'):
        if self.color_label is None:
            self.count_colors()
        if base_folder : 
            if not os.path.exists(base_folder):
                os.makedirs(base_folder)
            filename = base_folder             
        else: 
            filename = ''
        filename += "{}_{}.jpg".format(self.color_label,count)
        img = Image.fromarray(self.src)
        img.save(filename)
        return 