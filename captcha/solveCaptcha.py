from cv2 import cv2
import time
import pyautogui
import numpy as np
import mss
from os import listdir
from random import random, randint
import threading
# from skimage.metrics import structural_similarity


def remove_suffix(input_string, suffix):
    if suffix and input_string.endswith(suffix):
        return input_string[:-len(suffix)]
    return input_string

#TODO tirar duplicata
def load_images(dir_name):
    file_names = listdir(dir_name)
    targets = {}
    for file in file_names:
        path = dir_name + file
        targets[remove_suffix(file, '.png')] = cv2.imread(path)

    return targets

if __name__ == '__main__':
    d = load_images( './images/')
    s = load_images( './small-digits/')
else:
    d = load_images( './captcha/images/')
    s = load_images( './captcha/small-digits/')

#TODO tirar duplicata
def positions(target, threshold=0.88,img = None):
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

def getDigits(d,img, gray=True, threshold = 1):
    digits = []
    for i in range(10):
        if gray:
            template = cv2.cvtColor(d[str(i)], cv2.COLOR_BGR2GRAY)
        else:
            template = d[str(i)]

        p = positions(template,img=img,threshold=threshold)
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

def captchaImg(img, pos,w = 520, h = 180):
    # path = "./captchas-saved/{}.png".format(str(time.time()))
    rx, ry, _, _ = pos

    x_offset = -10
    y_offset = 140

    y = ry + y_offset
    x = rx + x_offset
    cropped = img[ y : y + h , x: x + w]
    return cropped

def smallDigitsImg(img, pos,w = 200, h = 70):
    # path = "./captchas-saved/{}.png".format(str(time.time()))
    rx, ry, _, _ = pos

    x_offset = 150
    y_offset = 80

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
        return None
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
def r():
    return randint(0,5)

def moveToReveal(popup_pos):
    # time.sleep(5)
    # return
    x,y,_,_ = popup_pos
    speed = 0.6
    offset_x = 30
    offset_y = 140
    w = 465
    h = 150
    passes = 9
    #11
    increment_x = w/passes
    increment_y = h/passes
    start_x = x + offset_x + r()
    start_y = y + offset_y + r()
    pyautogui.moveTo(start_x,start_y,speed)
    pyautogui.moveTo(start_x,start_y+h,speed)
    pyautogui.moveTo(start_x + w,start_y + h,speed)
    pyautogui.moveTo(start_x + w,start_y,speed)
    for i in range(passes):
        x = start_x + i * increment_x + r()
        y = start_y + h * (i % 2) + r()
        pyautogui.moveTo(x,y,speed)
    pyautogui.moveTo(start_x+ w + r(),start_y + h + r(),speed)
    time.sleep(1)

# def generateDiff(first,position):
    # gray_first = cv2.cvtColor(first, cv2.COLOR_BGR2GRAY)
    # screenshot = printSreen()
    # img = screenshot.copy()
    # second = captchaImg(img,position)
    # gray_second = cv2.cvtColor(second, cv2.COLOR_BGR2GRAY)


    # (_, diff) = structural_similarity(gray_first,gray_second, full=True)
    # diff = (diff * 255).astype("uint8")
    # cv2.imshow('img',diff)
    # cv2.waitKey(5000)

    # cv2.imshow('img',cp)
    # return diff

def preProcess(img,popup_pos):
    img = captchaImg(img, popup_pos[0])
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    t,img = cv2.threshold(img,170,240,cv2.THRESH_BINARY_INV)
    return img

def add(img0, img1):
    return cv2.bitwise_and(img0, img1, mask = None)

def getDiff(data):
    start = time.time()
    screenshots = []
    while data[1]:
        screenshot = printSreen()
        screenshots.append(screenshot)

    end = time.time()
    elapsed = end-start
    start = end
    i = len(screenshots)

    print('{} samples taken in {} seconds({}/s)'.format(i,elapsed,i/elapsed))
    popup_pos = positions(d['robot'],img=screenshot)
    preprocessed_data = [preProcess(s, popup_pos) for s in screenshots]
    end = time.time()
    elapsed = end-start
    start = end
    print('Processed {} images in {} seconds'.format(len(preprocessed_data),elapsed))
    result = preprocessed_data[0]
    for sample in preprocessed_data:
        result = add(result, sample)
    end = time.time()
    elapsed = end-start
    print('Combined {} images in {} seconds'.format(len(preprocessed_data),elapsed))
    # cv2.imshow('result',result)
    # cv2.waitKey(5000)
    data[0] = result
    return
        # time.sleep()

def watchDiffs(data):
    thread = threading.Thread(target=getDiff, args =(data,))
    thread.start()
    return thread
    # thread.join()


def getBackgroundText():
    screenshot = printSreen()
    popup_pos = positions(d['robot'],img=screenshot)
    data = [None,True]
    thread = watchDiffs(data)
    moveToReveal(popup_pos[0])
    # moveToReveal(popup_pos[0])
    data[1]=False
    thread.join()
    if __name__ == '__main__':
        path = "./tmp/{}.png".format(str(time.time()))
        cv2.imwrite(path,data[0])
    digits = getDigits(d,data[0],threshold = 0.9)

    return digits

def getSmallDigits(img, threshold=0.95,i=0):
    if __name__ == '__main__':
        path = "./tmp/small{}.png".format(str(time.time()))
        # cv2.imwrite(path,img)
    digits = getDigits(s,img, gray=False, threshold=threshold)

    if i > 10:
        if __name__ == '__main__':
            path = "./tmp/small{}.png".format(str(time.time()))
            cv2.imwrite(path,img)
            print('too many')
            print(digits)
        return [digits, threshold]

    if len(digits) == 3:
        return [digits, threshold]
    if len(digits) < 3:
        return getSmallDigits(img,threshold=threshold-0.3,i=i+1)
    if len(digits) > 3:
        return getSmallDigits(img,threshold=threshold+0.07,i=i+1)

def lookForMatch(background_digits,popup_pos, has_found):
        screenshot = printSreen()
        popup_pos = positions(d['robot'],img=screenshot)
        threshold = 0.95

        for i in range(100):
            screenshot = printSreen()
            captcha_img = smallDigitsImg(screenshot, popup_pos[0])
            small_digits, threshold = getSmallDigits(captcha_img, threshold=threshold)
            if small_digits == background_digits:
                pyautogui.mouseUp()
                print('FOUND!', flush=True)
                has_found[0] = True
                return

def solveCaptcha():
    screenshot = printSreen()
    img = screenshot.copy()
    popup_pos = positions(d['robot'],img=img)
    if len(popup_pos) == 0:
        print('no captcha popup found!')
        return
    img = captchaImg(img, popup_pos[0])
    background_digits = getBackgroundText()
    print('background = {}'.format(background_digits))
    x,y = position(d['slider'],img=screenshot)

    pyautogui.moveTo(x+r(),y+r(),0.8)
    has_found = [False]
    watcher = threading.Thread(target=lookForMatch, args =(background_digits,popup_pos,has_found))
    watcher.start()
    pyautogui.mouseDown()
    time.sleep(1)
    def movePercentage(n):
        current_x,_ = pyautogui.position()
        speed_factor = 2
        slider_size = 300
        destination = x+r()+n*slider_size
        randomness = random()/6
        speed = (abs(current_x - destination)/slider_size)*speed_factor + randomness
        pyautogui.moveTo(destination,y+r(),speed,pyautogui.easeOutQuad)

    randomness = random()/5
    movePercentage(.4+randomness)
    if has_found[0]:
        return
    randomness = random()/5
    movePercentage(-0.1+randomness)
    if has_found[0]:
        return
    randomness = random()/5
    movePercentage(1+randomness)
    if has_found[0]:
        return
    pyautogui.mouseUp()

    time.sleep(13)
    solveCaptcha()
    return

if __name__ == '__main__':
    solveCaptcha()
#TODO colocar positions em um arquivo separado e importar nos outros.
# tirar o load digits daqui e passar como argumento na funçao

        # (_, new_diff) = structural_similarity(img0,img1, full=True)
        # diff[0] = (new_diff * 255).astype("uint8")
# arrumar o mexer das posiçoes pra ele vazer mais movimentos verticais
# calcular n de sliders ou fazer recursivamente.
# fazer os and so no final
# fazer o bot pegar as top 3 imagens no get digits.
