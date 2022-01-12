from cv2 import cv2
import pyautogui
import mss
from os import listdir
from random import randint
import numpy as np
from skimage.metrics import structural_similarity
import time


from bomb_captcha_solver.yolov5.run import CaptchaSolver
def remove_suffix(input_string, suffix):
    if suffix and input_string.endswith(suffix):
        return input_string[:-len(suffix)]
    return input_string

def load_images():
    dir_name = './imgs/'
    file_names = listdir(dir_name)
    targets = {}
    for file in file_names:
        path = dir_name + file
        targets[remove_suffix(file, '.png')] = cv2.imread(path)

    return targets
d = load_images()

def printSreen():
    with mss.mss() as sct:
        monitor = sct.monitors[0]
        sct_img = np.array(sct.grab(monitor))
        # The screen part to capture
        # monitor = {"top": 160, "left": 160, "width": 1000, "height": 135}

        # Grab the data
        return sct_img[:,:,:3]

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


def captchaImg(img, pos,w = 500, h = 180):
    # path = "./captchas-saved/{}.png".format(str(time.time()))
    rx, ry, _, _ = pos

    x_offset = -10
    y_offset = 89

    y = ry + y_offset
    x = rx + x_offset
    cropped = img[ y : y + h , x: x + w]
    return cropped


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

def save(name,img):
    path = "./data/{}.png".format(name+'--'+str(time.time()))
    cv2.imwrite(path, img)
    # cv2.imshow(name,img)
    # cv2.waitKey(5000)

def moveSlider(screenshot, pos, popup_pos):
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

    pyautogui.moveTo(start_x+increment*pos ,start_y+randint(0,10),1)
    choice_images = []
    for i in range(5):
        choice_images.append(captchaImg(printSreen(),popup_pos[0]))
    # screenshot = printSreen()
    time.sleep(2)
    pyautogui.mouseUp()
    return choice_images


def getDiff(first,position):
    gray_first = cv2.cvtColor(first, cv2.COLOR_BGR2GRAY)
    screenshot = printSreen()
    img = screenshot.copy()
    second = captchaImg(img,position)
    gray_second = cv2.cvtColor(second, cv2.COLOR_BGR2GRAY)


    (_, diff) = structural_similarity(gray_first,gray_second, full=True)
    diff = (diff * 255).astype("uint8")
    # cv2.imshow('img',diff)
    # cv2.waitKey(5000)

    # cv2.imshow('img',cp)
    return diff
def outcome():
    img = printSreen()
    if not position(d['robot'], img=img) is None:
        return 'fail'
    if not position(d['connect-wallet'], img=img) is None:
        return 'success'
    if not position(d['timeout'], img=img) is None:
        return 'timeout'

def main():
    screenshot = printSreen()
    img = screenshot.copy()
    popup_pos = positions(d['robot'],img=img)
    if len(popup_pos) == 0:
        connect_wallet =  position(d['connect-wallet'],img=img)
        if connect_wallet is None:
            time.sleep(3)
            return
        (connect_x, connect_y) = connect_wallet
        pyautogui.moveTo(connect_x+randint(0,10),connect_y+randint(0,10),1)
        pyautogui.click()
        time.sleep(1)
        print('connect wallet')
        screenshot = printSreen()
        img = screenshot.copy()
        popup_pos = positions(d['robot'],img=img)
        if len(popup_pos) == 0:
            print('fail to open')
            pyautogui.hotkey('ctrl','f5')
            time.sleep(7)
            return
            # exit()

    first = captchaImg(img,popup_pos[0])
    awnser = getDigits(d,first)
    save('digits/'+awnser,first)
    # save(awnser,first)
    # exit()
    choice_screenshots = moveSlider(screenshot,randint(0,4),popup_pos)
    time.sleep(1)
    o = outcome()
    print('outcome %s' % o)
    if o == 'fail':
        for choice in choice_screenshots:
            save('fail/'+awnser,choice)
        # save in fails and continue
    if o == 'success':
        for choice in choice_screenshots:
            gray_first = cv2.cvtColor(first, cv2.COLOR_BGR2GRAY)
            gray_second = cv2.cvtColor(choice, cv2.COLOR_BGR2GRAY)
            (_, diff) = structural_similarity(gray_first,gray_second, full=True)
            diff = (diff * 255).astype("uint8")
            save('diff/'+awnser,diff)
        for choice in choice_screenshots:
            save('success/'+awnser,choice)
        pyautogui.click()
        pyautogui.hotkey('ctrl','f5')
        time.sleep(7)
        # save in success and refresh
    if o == 'timeout':
        for choice in choice_screenshots:
            save('fail/'+awnser,choice)
        time.sleep(10)
        # save in fail and wait

    # diff = getDiff(first,popup_pos[0])
    # save(awnser,diff)
    return
#TODO tirar o slider do print do resultado(diminuir h)
# pegar mais de uma imagem da escolha antes de soltar o mouse
# Salvar nas pastas success e fail com nome = numero, pensar em alternativa pro timestamp.


    i=0
    current = printSreen()
    while True:
        i = i + 1
        last = current
        current = printSreen()
        popup = positions(d['robot'],img=current)

        if len(popup) == 0:
            print('solved for {}!'.format(awnser))
            result = captchaImg(last, popup_pos[0],h = 400)
            break
    save(awnser,result)

cs = CaptchaSolver()
time.sleep(5)
img = printSreen()
popup_pos = positions(d['robot'],img=img)
img = captchaImg(img,popup_pos[0])
cp = CaptchaSolver()

print(cp.SolveCaptcha(img, "bomb_captcha_solver/yolov5/bomb_captcha.pt", 0.7))
exit()


# while True:
    # main()

# ret,thresh = cv2.threshold(gfirst,250,255,cv2.THRESH_BINARY)

