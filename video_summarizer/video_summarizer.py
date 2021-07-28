import cv2
import numpy as np

BLUR_SIZE = 5
THRESHOLD_SENSITIVITY = 30


def _difference_area(img1, img2) -> int:
    try:
        delta_frame = cv2.absdiff(img1, img2)
    except Exception:
        raise ValueError

    gray = cv2.cvtColor(delta_frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (BLUR_SIZE, BLUR_SIZE), 0)
    ret, th = cv2.threshold(blur, THRESHOLD_SENSITIVITY, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(th, np.ones((3, 3), np.uint8), iterations=3)

    c, h = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    return sum(cv2.contourArea(contour) for contour in c)


# === Movement detection ===============================================================================================

def detect_difference(img1, img2, area_threshold=250) -> bool:
    """Check if there is a difference in the two images.

    :param img1: previous image
    :param img2: present image
    :param area_threshold: sensitivity in pixel
    :return: True if the difference of the images is greater than the threshold, False otherwise.
    """

    return _difference_area(img1, img2) > area_threshold or False


def detect_difference_yeld(input_video_path, area_threshold=250) -> bool:
    raise NotImplementedError


def get_difference_area():
    raise NotImplementedError


def get_difference_roi():
    raise NotImplementedError


def get_difference_contours():
    raise NotImplementedError


# === Summarization ====================================================================================================

def summarize(video_input_path, video_output_path, mode, options):
    # todo usare interfaccia cli con progressbar
    pass


# === Heat Map =========================================================================================================

def heat_map(video_input_path, video_output_path, mode, options):
    # todo usare interfaccia cli con progressbar
    raise NotImplementedError
