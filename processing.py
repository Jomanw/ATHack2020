import cv2
import numpy as np

def adjust_gamma(image, gamma=1.0):
    invGamma = 1.0 / gamma
    table = np.array(np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8"))
    return cv2.LUT(image, table)

def no_process_frame(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.flip(image, 1)

    return image

def process_frame(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.flip(image, 1)

    return image

def process_threshold_frame(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(image,125, 255, cv2.THRESH_TOZERO_INV)
    return thresh

def process_filter_frame(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    image = cv2.filter2D(image, -1, kernel)
    return image

def process_contrast_frame(image, alpha, beta, enhance=False, sharpen=False, trace=False):
    # alpha = 1.0 # Contrast control (1.0-3.0)
    # beta = 0 # Brightness control (0-100)
    adjusted = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    adjusted = cv2.cvtColor(adjusted, cv2.COLOR_BGR2GRAY)
    if enhance:
        adjusted = cv2.equalizeHist(adjusted)
    if sharpen:
        kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        adjusted = cv2.filter2D(adjusted, -1, kernel)
    if trace:
        print("trace")
        adjusted = cv2.Canny(adjusted, 50, 150) # TODO: Make these parameters adjustable?
    return adjusted