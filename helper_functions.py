import cv2
import numpy as np
from config import *


def decrease_brightness_of_image(img, active: bool = False):
    if active:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        img[:, :, 2] = img[:, :, 2] * demo_modifier
        img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
    return img


def increase_contrast(img):
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

    l_channel, a, b = cv2.split(lab)

    # Applying CLAHE to L-channel
    # feel free to try different values for the limit and grid size:
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    cl = clahe.apply(l_channel)

    # merge the CLAHE enhanced L-channel with the a and b channel
    limg = cv2.merge((cl, a, b))

    # Converting image from LAB Color model to BGR color space
    enhanced_img = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

    return enhanced_img


def increase_visibility(img):
    img_hc = increase_contrast(img)
    LAB = cv2.cvtColor(img_hc, cv2.COLOR_BGR2LAB)

    L = LAB[:, :, 0]

    value, thresh = cv2.threshold(
        L, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_TRIANGLE)
    new_value = value + value_modifier

    thresh = cv2.threshold(L, new_value, 255, cv2.THRESH_BINARY)[1]
    thresh = 255 - thresh
    thresh = cv2.merge([thresh, thresh, thresh])

    blue = cv2.multiply(img_hc[:, :, 0], gain)
    green = cv2.multiply(img_hc[:, :, 1], gain)
    red = cv2.multiply(img_hc[:, :, 2], gain)
    img_bright = cv2.merge([blue, green, red])
    # TODO: apply cap to brightened pixels to prevent artifacts and overexposure
    result = np.where(thresh == 255, img_bright, img_hc)

    return result
