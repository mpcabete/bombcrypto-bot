from cv2 import cv2
import mss
import numpy as np

def getImageSize(img):
    return tuple(img.shape[1::-1])

def resizeImageForScale(image, scale=67):
    if image is not None:
        height, width = getImageSize(image)
        resize_size = (int(height * (scale/100)), int(width * (scale/100)))
        resized = cv2.resize(image, resize_size, interpolation= cv2.INTER_LINEAR)
        return resized
    return image

def printScreen():
    with mss.mss() as sct:
        monitor = sct.monitors[0]
        sct_img = np.array(sct.grab(monitor))
        return sct_img[:,:,:3]

def printScreenForWindow(window, activate=False):
    if activate:
        window.activate()
    width, height = window.size
    left = window.left
    top = window.top

    with mss.mss() as sct:
        monitor = sct.monitors[0]
        monitor = {"top": top, "left": left, "width": width, "height": height}
        sct_img = np.array(sct.grab(monitor))
        return sct_img[:,:,:3]