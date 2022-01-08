from cv2 import cv2
import numpy as np
import mss

def show(rectangles, img = None, title='img'):
    if img is None:
        with mss.mss() as sct:
            monitor = sct.monitors[0]
            img = np.array(sct.grab(monitor))

    for (x, y, w, h) in rectangles:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255,255,255,255), 2)

    cv2.imshow(title,img)
    cv2.waitKey(0)
