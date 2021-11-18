import mss
import numpy as np
from cv2 import cv2
import pyautogui



golden = cv2.imread('targets/chest-golden-nolife.png')
wooden = cv2.imread('targets/chest-wooden-nolife.png')
plate = cv2.imread('targets/chest-plate-nolife.png')


go_work_img = cv2.imread('targets/go-work.png')
commom_img = cv2.imread('targets/commom-text.png')
arrow_img = cv2.imread('targets/go-back-arrow.png')
hero_img = cv2.imread('targets/hero-icon.png')
x_button_img = cv2.imread('targets/x.png')
teasureHunt_icon_img = cv2.imread('targets/treasure-hunt-icon.png')
ok_btn_img = cv2.imread('targets/ok.png')
connect_wallet_btn_img = cv2.imread('targets/connect-wallet.png')
select_wallet_hover_img = cv2.imread('targets/select-wallet-1-hover.png')
select_metamask_no_hover_img = cv2.imread('targets/select-wallet-1-no-hover.png')
sign_btn_img = cv2.imread('targets/select-wallet-2.png')
new_map_btn_img = cv2.imread('targets/new-map.png')
green_bar = cv2.imread('targets/green-bar.png')

def show_image(image):
    cv2.imshow("images", image)

def draw_rectangles(image, rectangles):
    for x, y, w, h in rectangles:
        image = cv2.rectangle(image.astype(np.int32), (x, y), (x+w, y+h), (0, 0, 255), 10)
    return image.astype(np.uint8)

def crop_image(image, x, y, w, h):
    return image[y:y+h, x:x+w]

with mss.mss() as sct:
    sct_img = np.array(sct.grab(sct.monitors[0]))
    img = sct_img[:,:,:3]


orig = img.copy()
for target in (green_bar):
    result = cv2.matchTemplate(orig, target,cv2.TM_CCOEFF_NORMED)
    w = target.shape[1]
    h = target.shape[0]

    yloc, xloc = np.where(result >= 0.6)


    rectangles = []
    for (x, y) in zip(xloc, yloc):
        rectangles.append([int(x), int(y), int(w), int(h)])
        rectangles.append([int(x), int(y), int(w), int(h)])

    rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)

    img = draw_rectangles(img, rectangles)
show_image(img)
cv2.waitKey(0)

def printSreen():
    with mss.mss() as sct:
        # The screen part to capture
        monitor = {"top": 160, "left": 160, "width": 1000, "height": 135}

        # Grab the data
        #sct_img = np.array(sct.grab(monitor))
        sct_img = np.array(sct.grab(sct.monitors[0]))
        return sct_img[:,:,:3]

def positions(target, trashhold=0.7):
    img = printSreen()
    result = cv2.matchTemplate(img,target,cv2.TM_CCOEFF_NORMED)
    w = target.shape[1]
    h = target.shape[0]

    yloc, xloc = np.where(result >= trashhold)


    rectangles = []
    for (x, y) in zip(xloc, yloc):
        rectangles.append([int(x), int(y), int(w), int(h)])
        rectangles.append([int(x), int(y), int(w), int(h)])

    rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)
    return rectangles

global off_x
off_x = 0
with mss.mss() as sct:
    off_x = 0
    if(len(sct.monitors) == 3):
        monitor = sct.monitors[2]
        off_x = -monitor['width']

def fun_move(x,y,duration):
    pyautogui.moveTo(x + off_x,y,duration)

def isWorking(bar, buttons):
    y = bar[1]

    for (_,button_y,_,button_h) in buttons:
        isBelow = y < (button_y + button_h)
        isAbove = y > (button_y - button_h)
        if isBelow and isAbove:
            return False
    return True

def clickGreenBarButtons():
    # ele clicka nos q tao trabaiano mas axo q n importa
    offset = 130
    green_bars = positions(green_bar, trashhold=0.9)
    buttons = positions(go_work_img, trashhold=0.9)

    not_working_green_bars = []
    for bar in green_bars:
        if not isWorking(bar, buttons):
            not_working_green_bars.append(bar)

    # se tiver botao com y maior que bar y-10 e menor que y+10
    for (x, y, w, h) in not_working_green_bars:
        # isWorking(y, buttons)
        fun_move(x+offset+(w/2),y+(h/2),1)
        global hero_clicks
        hero_clicks = hero_clicks + 1
        #cv2.rectangle(sct_img, (x, y) , (x + w, y + h), (0,255,255),2)
    return len(not_working_green_bars)

clickGreenBarButtons()