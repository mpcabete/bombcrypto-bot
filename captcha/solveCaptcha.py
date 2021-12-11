from cv2 import cv2
import time
import pyautogui
import numpy as np
import mss
from os import listdir
# from run import getBackgroundText
import torch
from random import randint

# example_captcha_img = cv2.imread('images/example.png')

model = torch.hub.load('./captcha', 'custom', "captcha/bomb_captcha.pt", source='local')

def getBackgroundText(img, percent_required):
    boxes = []
    if type(img) == np.ndarray  and percent_required:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        results = model(img, size=416)
        digits = []

        if results.xyxy[0].shape[0] >= 1:
            for box in results.xyxy[0]:
                x1, _, _, _, percent, digit = box
                if percent >= percent_required:
                    digits.append({'x':x1.item(), 'd':digit.item()})

            def getX(e):
                return e['x']
            digits.sort(key=getX)

            def getD(e):
                return str(int(e['d']))

            return ''.join(list(map(getD, digits)))

def remove_suffix(input_string, suffix):
    if suffix and input_string.endswith(suffix):
        return input_string[:-len(suffix)]
    return input_string

#TODO tirar duplicata
def load_images():
    dir_name = './captcha/images/'
    file_names = listdir(dir_name)
    targets = {}
    for file in file_names:
        path = dir_name + file
        targets[remove_suffix(file, '.png')] = cv2.imread(path)

    return targets
d = load_images()

#TODO tirar duplicata
def positions(target, threshold=0.85,img = None):
    if img is None:
        img = printSreen()
    result = cv2.matchTemplate(img,target,cv2.TM_CCOEFF_NORMED)
    w = target.shape[1]
    h = target.shape[0]

    yloc, xloc = np.where(result >= threshold)


    rectangles = []
    for (x, y) in zip(xloc, yloc):
        rectangles.append([int(x), int(y), int(w), int(h)])
        rectangles.append([int(x), int(y), int(w), int(h)])

    rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)
    return rectangles

def getDigits(d,img):
    digits = []
    for i in range(10):
        p = positions(d[str(i)],img=img,threshold=0.95)
        if len (p) > 0:
            digits.append({'digit':str(i),'x':p[0][0]})

    def getX(e):
        return e['x']

    digits.sort(key=getX)
    r = list(map(lambda x : x['digit'],digits))
    return(''.join(r))
    # getFirstDigits(first)

def printSreen():
    with mss.mss() as sct:
        monitor = sct.monitors[0]
        sct_img = np.array(sct.grab(monitor))
        # The screen part to capture
        # monitor = {"top": 160, "left": 160, "width": 1000, "height": 135}

        # Grab the data
        return sct_img[:,:,:3]

def captchaImg(img, pos,w = 500, h = 180):
    # path = "./captchas-saved/{}.png".format(str(time.time()))
    rx, ry, _, _ = pos

    x_offset = -10
    y_offset = 89

    y = ry + y_offset
    x = rx + x_offset
    cropped = img[ y : y + h , x: x + w]
    return cropped

def position(target, threshold=0.85,img = None):
    if img is None:
        img = printSreen()
    result = cv2.matchTemplate(img,target,cv2.TM_CCOEFF_NORMED)
    w = target.shape[1]
    h = target.shape[0]

    yloc, xloc = np.where(result >= threshold)


    rectangles = []
    for (x, y) in zip(xloc, yloc):
        rectangles.append([int(x), int(y), int(w), int(h)])
        rectangles.append([int(x), int(y), int(w), int(h)])

    rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)
    if len(rectangles) > 0:
        x,y, w,h = rectangles[0]
        return (x+(w/2),y+h/2)

def getSliderPositions(screenshot, popup_pos):
    slider = position(d['slider'],img=screenshot)

    if slider is None:
        print('no slider')
        exit()
    (start_x, start_y) = slider

    pyautogui.moveTo(start_x,start_y+randint(0,10),1)
    pyautogui.mouseDown()
    pyautogui.moveTo(start_x+400,start_y+randint(0,10),1)

    screenshot = printSreen()

    end = position(d['slider'],img=screenshot,threshold = 0.8)
    (end_x, end_y) = end


    size = end_x-start_x

    increment = size/4

    positions = []
    for i in range(5):
        # pyautogui.moveTo(start_x+increment*pos ,start_y+randint(0,10),1)
        positions.append((start_x+increment*i ,start_y+randint(0,10)))
        # screenshot = printSreen()
        # time.sleep(2)
        # pyautogui.mouseUp()
    return positions


def solveCaptcha():
    screenshot = printSreen()
    img = screenshot.copy()
    popup_pos = positions(d['robot'],img=img)
    print(popup_pos)
    if len(popup_pos) == 0:
        print('no captcha popup found!')
        return
    img = captchaImg(img, popup_pos[0])
    digits = getDigits(d, img)
    slider_positions = getSliderPositions(screenshot, popup_pos)
    # moveSlider(screenshot,3,popup_pos)


    for position in slider_positions:
        x, y = position
        pyautogui.moveTo(x,y,1)
        screenshot = printSreen()
        popup_pos = positions(d['robot'],img=screenshot)
        captcha_img = captchaImg(screenshot, popup_pos[0])
        # captcha_img = example_captcha_img
        background_digits = getBackgroundText(captcha_img,  0.7)
        print( 'dig: {}, background_digits: {}'.format(digits, background_digits))
        if digits == background_digits:
            print('FOUND!')
            pyautogui.mouseUp()
            return

if __name__ == '__main__':
    solveCaptcha()
#TODO colocar positions em um arquivo separado e importar nos outros.
# tirar o load digits daqui e passar como argumento na funçao

