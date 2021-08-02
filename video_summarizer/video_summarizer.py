import os

import cv2
import numpy as np
from tqdm import tqdm

SUPPORTED_MODES_OPTIONS = {
    0: {"name": "motion", "desc": "Save only frame that contains difference from the previous frame"}
}

SUPPORTED_FORMATS = ("mp4",)

BLUR_SIZE = 5
THRESHOLD_SENSITIVITY = 30


def _get_difference_area(img1, img2) -> int:
    """Get the difference area between two images in pixels.

    Uses cv2.absdiff() between the two images.

    :param img1: First image
    :param img2: Second image
    :return: Difference area in pixels
    """
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

    return _get_difference_area(img1, img2) > area_threshold or False


def detect_difference_yeld(input_video_path, area_threshold=250) -> bool:
    raise NotImplementedError


def get_difference_area():
    raise NotImplementedError


def get_difference_roi():
    raise NotImplementedError


def get_difference_contours():
    raise NotImplementedError


# === Summarization ====================================================================================================

def summarize(input_video_path: str, output_video_path: str, mode: str, options=None, movement_threshold=250,
              verbose=True):
    # TODO option parameter to raise exception when outputfile exists
    if not os.path.exists(input_video_path):
        raise FileNotFoundError(f"Input file {input_video_path} not found.")

    if not input_video_path.endswith(SUPPORTED_FORMATS):
        print("[ERROR] Input file format not supported")
        return

    if not output_video_path.endswith(SUPPORTED_FORMATS):
        print("[ERROR] Processed file format not supported")
        return

    if mode == SUPPORTED_MODES_OPTIONS[0]["name"]:
        _motion_summarization(input_video_path, output_video_path, movement_threshold, verbose)
    else:
        print(f"[INFO] mode [{mode}] don't exist. "
              f"Supported mode options: {[mode['name'] for mode in SUPPORTED_MODES_OPTIONS.values()]}")


def _motion_summarization(input_video_path: str, output_video_path: str, movement_threshold: int, verbose: bool):
    first_frame = None
    cap = cv2.VideoCapture(input_video_path)

    if not cap.isOpened():
        print(f"[ERROR] Error opening video file {input_video_path}")
        return None
    else:
        vid_info = _get_video_info(cap)
        video_writer = cv2.VideoWriter(output_video_path, vid_info["fourcc"], vid_info["fps"], vid_info["size"], True)

    print(f"[PROCESSING video '{input_video_path}' to '{output_video_path}']")
    progress_bar = tqdm(total=vid_info["frame_count"])

    while cap.isOpened():

        ret, frame = cap.read()
        if not ret:
            break

        mov = _something_moves(first_frame, frame, movement_threshold)
        first_frame = frame.copy()

        if mov:
            video_writer.write(frame)

        progress_bar.update(1)

    progress_bar.close()
    cap.release()
    video_writer.release()

    if verbose:
        _print_conclusion(input_video_path, output_video_path)


# === Heat Map =========================================================================================================

def heat_map(video_input_path, video_output_path, mode, options):
    raise NotImplementedError


# === Utils ============================================================================================================

def _print_conclusion(input_video_path: str, output_video_path: str):
    """Print the results of the operation.

    :param input_video_path: path of the video before processing.
    :param output_video_path: path of the video after processing.
    :return:
    """
    print("[PROCESS COMPLETED]")

    input_video_duration = _get_video_info(cv2.VideoCapture(input_video_path))["duration"]
    output_video_duration = _get_video_info(cv2.VideoCapture(output_video_path))["duration"]

    print(f"[INFO] Your input video file is {input_video_duration}")
    print(f"[INFO] Your output video file is {output_video_duration}")


def _get_video_info(video_capture: cv2.VideoCapture):
    """Get video details.

    Details:

    - frames size (size)
    - fps (fps)
    - number of frames (frame_count)
    - duration (duration)
    - fourcc codec (fourcc)

    :param video_capture: cv2.VideoCapture object of the video.
    :return: Details of the VideoCapture video.
    """

    # todo add hour to duration

    fps = video_capture.get(cv2.CAP_PROP_FPS)
    frame_count = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
    size = (int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    fourcc = int(video_capture.get(cv2.CAP_PROP_FOURCC))

    duration = frame_count / fps
    minutes = int(duration / 60)
    seconds = int(duration % 60)

    return {"size": size, "fps": fps, "frame_count": frame_count, "duration": f"{minutes}'{seconds}\"", "fourcc": fourcc}
