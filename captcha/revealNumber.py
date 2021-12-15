# You can donate to me :D
# Smart Chain Wallet: 0x0A11264F89F985E9FA60e989A2C4A5E0FCFE9345

from cv2 import cv2
import time
import pyautogui
import numpy as np
import mss
from os import listdir
from random import randint


def remove_suffix(input_string, suffix):
    if suffix and input_string.endswith(suffix):
        return input_string[:-len(suffix)]
    return input_string


def load_images():
    dir_name = './captcha/images/'
    file_names = listdir(dir_name)
    targets = {}
    for file in file_names:
        path = dir_name + file
        targets[remove_suffix(file, '.png')] = cv2.imread(path)

    return targets


d = load_images()
saved_image_index = 0


def positions(target, threshold=0.85, img=None):
    if img is None:
        img = printSreen()
    result = cv2.matchTemplate(img, target, cv2.TM_CCOEFF_NORMED)
    w = target.shape[1]
    h = target.shape[0]

    yloc, xloc = np.where(result >= threshold)

    rectangles = []
    for (x, y) in zip(xloc, yloc):
        rectangles.append([int(x), int(y), int(w), int(h)])
        rectangles.append([int(x), int(y), int(w), int(h)])

    rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)
    return rectangles


def getDigits(img, prefix='', invert=False):
    # global saved_image_index
    # cv2.imwrite(
    #     './captchas-saved/{}-{}-original.png'.format(str(time.time()), saved_image_index), img)

    (thresh, bw) = cv2.threshold(img, 127,
                                 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    if invert:
        bw = cv2.bitwise_not(bw)
    img = cv2.cvtColor(bw, cv2.COLOR_GRAY2BGR)

    # cv2.imwrite(
    #     './captchas-saved/{}-{}-bw.png'.format(str(time.time()), saved_image_index), img)
    # saved_image_index += 1

    digits = []
    for i in range(10):
        p = positions(d[prefix+str(i)], img=img, threshold=0.86)
        for j in range(len(p)):
            digits.append({'digit': str(i), 'x': p[j][0]})

    def getX(e):
        return e['x']

    digits.sort(key=getX)
    r = list(map(lambda x: x['digit'], digits))

    return(''.join(r))


def printSreen():
    with mss.mss() as sct:
        monitor = sct.monitors[0]
        sct_img = np.array(sct.grab(monitor))
        # The screen part to capture
        # monitor = {"top": 160, "left": 160, "width": 1000, "height": 135}

        # Grab the data
        return sct_img[:, :, :3]


def captchaImg(img, pos, w=300, h=65, x_offset=100, y_offset=85):
    rx, ry, _, _ = pos
    y = ry + y_offset
    x = rx + x_offset
    cropped = img[y: y + h, x: x + w, 2]
    return cropped


def revealCaptchaImg(pos, w=500, h=200, x_offset=-10, y_offset=140):
    img = printSreen().copy()
    revealImg = captchaImg(img, pos, w, h, x_offset, y_offset)

    rx, ry, _, _ = pos
    y = ry + y_offset
    x = rx + x_offset

    for i in range(y+30, y+h, 30):
        for j in range(x+50, x+w, 30):
            pyautogui.moveTo(j/2, i/2, 0.1)
            img = printSreen().copy()
            revealImg = np.maximum(
                revealImg,
                captchaImg(img, pos, w, h, x_offset, y_offset),
            )

    return revealImg


def position(target, threshold=0.85, img=None):
    if img is None:
        img = printSreen()
    result = cv2.matchTemplate(img, target, cv2.TM_CCOEFF_NORMED)
    w = target.shape[1]
    h = target.shape[0]

    yloc, xloc = np.where(result >= threshold)

    rectangles = []
    for (x, y) in zip(xloc, yloc):
        rectangles.append([int(x), int(y), int(w), int(h)])
        rectangles.append([int(x), int(y), int(w), int(h)])

    rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)
    if len(rectangles) > 0:
        x, y, w, h = rectangles[0]
        return (x+(w/2), y+h/2)


def getSliderPositions(screenshot, popup_pos):
    slider = position(d['slider'], img=screenshot)

    if slider is None:
        print('no slider')
        return None
    (start_x, start_y) = slider

    pyautogui.moveTo(start_x/2, (start_y+randint(0, 10))/2, 1)
    pyautogui.mouseDown()
    pyautogui.moveTo((start_x+400)/2, (start_y+randint(0, 10))/2, 1)

    screenshot = printSreen()

    end = position(d['slider'], img=screenshot, threshold=0.8)
    (end_x, end_y) = end

    size = end_x-start_x

    increment = size/4

    positions = []
    for i in range(5):
        # pyautogui.moveTo((start_x+increment*pos)/2 ,(start_y+randint(0,10))/2,1)
        positions.append((start_x+increment*i, start_y+randint(0, 10)))
        # screenshot = printSreen()
        # time.sleep(2)
        # pyautogui.mouseUp()
    return positions


def solveCaptcha():
    screenshot = printSreen()
    img = screenshot.copy()
    popup_pos = positions(d['robot'], img=img)

    if len(popup_pos) == 0:
        print('no captcha popup found!')
        return

    img = revealCaptchaImg(popup_pos[0])
    target = getDigits(img, prefix='rn-target-', invert=True)
    print('target number:', target)

    # cv2.imshow('Target', img)
    # cv2.waitKey(0)

    slider_positions = getSliderPositions(screenshot, popup_pos)
    if slider_positions is None:
        return

    for index, position in enumerate(slider_positions):
        x, y = position
        pyautogui.moveTo(x/2, y/2, 1)
        screenshot = printSreen()
        popup_pos = positions(d['robot'], img=screenshot)
        img = captchaImg(screenshot, popup_pos[0])
        choice = getDigits(img, prefix='rn-choice-')
        print('choice number #{}:'.format(index+1), choice)

        # cv2.imshow('choice', img)
        # cv2.waitKey(0)

        if choice == target:
            print('FOUND!')
            pyautogui.mouseUp()
            return

    print('not found... trying again!')
    pyautogui.mouseUp()
    time.sleep(3)
    solveCaptcha()

    return


if __name__ == '__main__':
    solveCaptcha()
