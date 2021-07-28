import cv2
import numpy as np
from tqdm import tqdm

SUPPORTED_MODE_OPTIONS = {"movement": "Save only frame that contains difference from the previous frame"}
SUPPORTED_FORMATS = ["mp4"]

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


def _something_moves(first_frame, img, movement_threshold=250):
    try:
        movement = detect_difference(first_frame, img, movement_threshold)
    except ValueError:
        first_frame = img
        movement = detect_difference(first_frame, img, movement_threshold)

    return movement


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

def summarize(input_video_path, output_video_path, mode, options=None, movement_threshold=250, verbose=True):
    if mode == "movement":
        _movement_summarization(input_video_path, output_video_path, movement_threshold, verbose)
    else:
        print(f"[INFO] mode <{mode}> don't exist. "
              f"Supported mode options: {[mode for mode in SUPPORTED_MODE_OPTIONS.keys()]}")


def _movement_summarization(input_video_path, output_video_path, movement_threshold, verbose):
    video_writer = None
    first_frame = None
    cap = cv2.VideoCapture(input_video_path)

    if not cap.isOpened():
        print(f"[ERROR] Error opening video file {input_video_path}")
        return None
    else:
        video_info = _get_video_info(cap)

        fourcc = 0x7634706d
        video_writer = cv2.VideoWriter(output_video_path, fourcc, video_info["fps"], video_info["size"], True)

    pbar = tqdm(total=video_info["frame_count"])
    while cap.isOpened():

        ret, frame = cap.read()
        if not ret:
            break

        mov = _something_moves(first_frame, frame, movement_threshold)
        first_frame = frame.copy()

        if mov:
            video_writer.write(frame)

        pbar.update(1)

    pbar.close()
    cap.release()
    video_writer.release()

    if verbose:
        _print_conclusion(input_video_path, output_video_path)


# === Heat Map =========================================================================================================

def heat_map(video_input_path, video_output_path, mode, options):
    # todo usare interfaccia cli con progressbar
    raise NotImplementedError


# === Utils ============================================================================================================

def _print_conclusion(input_video_path, output_video_path):
    print("[COMPLETED]")

    input_video_duration = _get_video_info(cv2.VideoCapture(input_video_path))["duration"]
    output_video_duration = _get_video_info(cv2.VideoCapture(output_video_path))["duration"]

    print(f"[INFO] Your input video file is {input_video_duration}")
    print(f"[INFO] Your output video file is {output_video_duration}")


def _get_video_info(video_capture):
    fps = video_capture.get(cv2.CAP_PROP_FPS)
    frame_count = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
    size = (int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    duration = frame_count / fps
    minutes = int(duration / 60)
    seconds = int(duration % 60)

    return {"size": size, "fps": fps, "frame_count": frame_count, "duration": f"{minutes}:{seconds}"}
