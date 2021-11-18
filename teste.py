import mss
import numpy as np
from cv2 import cv2



target = cv2.imread('targets/go-back-arrow.png')

def show_image(image):
    cv2.imshow("images", image)

with mss.mss() as sct:
    sct_img = np.array(sct.grab(sct.monitors[0]))
    img = sct_img[:,:,:3]

result = cv2.matchTemplate(img,target,cv2.TM_CCOEFF_NORMED)
w = target.shape[1]
h = target.shape[0]

yloc, xloc = np.where(result >= 0.7)


rectangles = []
for (x, y) in zip(xloc, yloc):
    rectangles.append([int(x), int(y), int(w), int(h)])
    rectangles.append([int(x), int(y), int(w), int(h)])

rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)

def draw_rectangles(image, rectangles):
    for x, y, w, h in rectangles:
        image = cv2.rectangle(image.astype(np.int32), (x, y), (x+w, y+h), (0, 0, 255), 10)
    return image.astype(np.uint8)

def crop_image(image, x, y, w, h):
    return image[y:y+h, x:x+w]

# img_retangle = draw_rectangles(img, rectangles)
# show_image(img_retangle)
# cv2.waitKey(0)


off_x = 0
if(len(sct.monitors) == 3):
    monitor = sct.monitors[3]
    off_x = monitor['width']
