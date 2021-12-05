from cv2 import cv2
import numpy as np
import mss
import pyautogui
import time
import sys
from random import randint
import yaml
#import requests
import logger

puzzle_img = cv2.imread('targets/puzzle.png')
piece = cv2.imread('targets/piece.png')
robot = cv2.imread('targets/robot.png')
slider = cv2.imread('targets/slider.png')
stream = open("config.yaml", 'r')
c = yaml.safe_load(stream)
ct = c['threshold']
number_of_matchs = 0

def printSreen():
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        sct_img = np.array(sct.grab(monitor))
        return sct_img[:,:,:3]
    
def positions(target, threshold=ct['default']):
    img = printSreen()
    result = cv2.matchTemplate(img.astype(np.uint8),target,cv2.TM_CCOEFF_NORMED)    
    w = target.shape[1]
    h = target.shape[0]

    yloc, xloc = np.where(result >= threshold)

    rectangles = []
    for (x, y) in zip(xloc, yloc):
        rectangles.append([int(x), int(y), int(w), int(h)])
        rectangles.append([int(x), int(y), int(w), int(h)])

    rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)
    return rectangles

def sobelOperator(img):
    scale = 1
    delta = 0
    ddepth = cv2.CV_16S
    img = cv2.GaussianBlur(img, (3, 3), 0)
    gray = img
    grad_x = cv2.Sobel(gray, ddepth, 1, 0, ksize=3, scale=scale, delta=delta, borderType=cv2.BORDER_DEFAULT)
    grad_y = cv2.Sobel(gray, ddepth, 0, 1, ksize=3, scale=scale, delta=delta, borderType=cv2.BORDER_DEFAULT)
    abs_grad_x = cv2.convertScaleAbs(grad_x)
    abs_grad_y = cv2.convertScaleAbs(grad_y)
    grad = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
    return cv2.cvtColor(grad, cv2.COLOR_BGR2GRAY)

def findPuzzlePieces(result, piece_img, threshold=0.5):
    piece_w = piece_img.shape[1]
    piece_h = piece_img.shape[0]
    yloc, xloc = np.where(result >= threshold)
    r= []
    for (piece_x, piece_y) in zip(xloc, yloc):
        r.append([int(piece_x), int(piece_y), int(piece_w), int(piece_h)])
        r.append([int(piece_x), int(piece_y), int(piece_w), int(piece_h)])
    r, weights = cv2.groupRectangles(r, 1, 0.2)
    if len(r) < 2:
        logger.logger('threshold = %.3f' % threshold)
        return findPuzzlePieces(result, piece_img,threshold-0.01)
    if len(r) == 2:
        print(number_of_matchs)
        logger.logger('match -> total of matchs is ',number_of_matchs)
        return r
    if len(r) > 2:
        logger.logger('overshoot by %d' % len(r))
        return r

def getRightPiece(puzzle_pieces):
    xs = [row[0] for row in puzzle_pieces]
    index_of_right_rectangle = xs.index(max(xs))
    right_piece = puzzle_pieces[index_of_right_rectangle]
    return right_piece

def getLeftPiece(puzzle_pieces):
    xs = [row[0] for row in puzzle_pieces]
    index_of_left_rectangle = xs.index(min(xs))
    left_piece = puzzle_pieces[index_of_left_rectangle]
    return left_piece

def show(rectangles, img = None):
    if img is None:
        with mss.mss() as sct:
            monitor = sct.monitors[0]
            img = np.array(sct.grab(monitor))
    for (x, y, w, h) in rectangles:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255,255,255,255), 2)
    cv2.imshow('img',img)
    cv2.waitKey(0)

def getPiecesPosition(t = 150):
    popup_pos = positions(robot)
    if len(popup_pos) == 0:
        logger.logger('puzzle not found')
        return
    rx, ry, _, _ = popup_pos[0]
    w = 380
    h = 200
    x_offset = -40
    y_offset = 65
    y = ry + y_offset
    x = rx + x_offset
    img = printSreen()
    cropped = img[ y : y + h , x: x + w]
    blurred = cv2.GaussianBlur(cropped, (3, 3), 0)
    edges = cv2.Canny(blurred, threshold1=t/2, threshold2=t,L2gradient=True)
    piece_img = cv2.cvtColor(piece, cv2.COLOR_BGR2GRAY)
    print('----')
    print(piece_img.shape)
    print(edges.shape)
    print('----')
    result = cv2.matchTemplate(edges,piece_img,cv2.TM_CCORR_NORMED)
    puzzle_pieces = findPuzzlePieces(result, piece_img)
    if puzzle_pieces is None:
        return
    absolute_puzzle_pieces = []
    for i, puzzle_piece in enumerate(puzzle_pieces):
        px, py, pw, ph = puzzle_piece
        absolute_puzzle_pieces.append( [ x + px, y + py, pw, ph])
    absolute_puzzle_pieces = np.array(absolute_puzzle_pieces)
    return absolute_puzzle_pieces

def getSliderPosition():
    slider_pos = positions(slider)
    if len (slider_pos) == 0:
        return False
    x, y, w, h = slider_pos[0]
    position = [x+w/2,y+h/2]
    return position

def solveCaptcha():
    pieces_start_pos = getPiecesPosition()
    if pieces_start_pos is None :
        return
    slider_start_pos = getSliderPosition()
    x,y = slider_start_pos
    pyautogui.moveTo(x,y,1)
    pyautogui.mouseDown()
    pyautogui.moveTo(x+300 ,y,0.5)
    pieces_end_pos = getPiecesPosition()
    piece_start, _, _, _ = getLeftPiece(pieces_start_pos)
    piece_end, _, _, _ = getRightPiece(pieces_end_pos)
    piece_middle, _, _, _  = getRightPiece(pieces_start_pos)
    slider_start, _, = slider_start_pos
    slider_end, _ = getSliderPosition()
    print (piece_start)
    print (piece_end)
    print (piece_middle)
    print (slider_start)
    print (slider_end)
    piece_domain = piece_end - piece_start
    middle_piece_in_percent = (piece_middle - piece_start)/piece_domain
    print('middle_piece_in_percent{} '.format(middle_piece_in_percent ))
    slider_domain = slider_end - slider_start
    slider_awnser = slider_start + (middle_piece_in_percent * slider_domain)
    pyautogui.moveTo(slider_awnser,y,0.5)
    pyautogui.mouseUp()