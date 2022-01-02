from cv2 import cv2
from os import listdir
import src.env as env
from src.utils import string

def loadHeroesToSendHome():
    file_names = listdir('./targets/heroes-to-send-home')
    heroes = []
    for file in file_names:
        path = './targets/heroes-to-send-home/' + file
        # TODO: add scale?
        hero_image = cv2.imread(path)
        heroes.append(hero_image)

    print('>>---> %d heroes that should be sent home loaded' % len(heroes))
    return heroes

def load_images():
    file_names = listdir('./targets/')
    targets = {}
    for file in file_names:
        path = 'targets/' + file
        target_name = string.remove_suffix(file, '.png')
        temp_image = cv2.imread(path)
        if env.scale_image['enable']:
            targets[target_name] = resize_image(temp_image, env.scale_image['percent'])
        else:
            targets[target_name] = temp_image

    return targets