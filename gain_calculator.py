import matplotlib.pyplot as plt
import cv2 
import imutils
from imutils.perspective import four_point_transform
from imutils import contours as cnts
import numpy as np

class Comparator:
    def __init__(self):
        
        self.digit_targets = {x:import_preprocess_image(f'targets/number_images/{x}.png', crop=True) 
                              for x in range(10)}
         
        
    def compare(self, input_img):
        
        accuracy_vector = np.zeros(10)
        # manage 1
        for digit in self.digit_targets.keys():
            if digit != 1:                
                acc_digit = cv2.matchTemplate(input_img, self.digit_targets[digit],cv2.TM_CCOEFF_NORMED)
                #print(acc_digit.flatten())
                accuracy_vector[digit] = acc_digit.flatten()[0]
        #print(accuracy_vector)
        
        # 1 digit handling
        if (np.max(accuracy_vector) <= 0.85):
            accuracy_vector[1] = 0.99      
        
        
        return np.argmax(accuracy_vector)

def import_preprocess_image(path, crop=False):
    image = cv2.imread(path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 50, 200, 255)
    
    if crop:
        digit_loc = find_digits_locations(edged)
        #print(digit_loc)
        edged = get_crops(edged, digit_loc)[0]
        
    #plt.imshow(edged, cmap='gray')
    
    return edged

def preprocess_image(img):
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 50, 200, 255)
    
    return edged

def find_digits_locations(img):
    
    countours = cv2.findContours(img.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    countours = imutils.grab_contours(countours)
    digit_countours = []
    digit_xy = []

    for c in countours:
        (x, y, w, h) = cv2.boundingRect(c)
        if (w>= 12 and w<=28) and (h>= 24 and h<= 26):
            digit_countours.append(c)
            if (x, y, w, h) not in digit_xy:
                digit_xy.append((x, y, w, h))
            
    return digit_xy

def filter_digits(digit_xy):
    
    # filter the location list
    y_coord = []
    for tup in digit_xy:
        y_coord.append(tup[1])

    uniques, counts = np.unique(y_coord, return_counts=True)
    digits_y = uniques[np.argmax(counts)]

    #print(uniques, counts)

    result = []
    
    for tup in digit_xy:
        if tup[1] == digits_y:
            result.append(tup)
    
    return result

def get_crops(img, digit_xy):
    
    digit_crop = []
    for coor in digit_xy:
        x,y,w,h = coor
        digit_crop.append(img.copy()[y:y+25, x:x+21])
    
    return digit_crop


def compute_results(digit_crops):
    
    comparator = Comparator()
    
    # usually they are in reversed order and the first one 
    # must be discarded since it is the number of heroes

    results = [comparator.compare(x) for x in digit_crops[1:]]

    s = ''
    for digit in reversed(results):
        if len(s) == 2:
            s += '.'
        s += str(digit)

    return float(s)
    


