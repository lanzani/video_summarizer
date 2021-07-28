import cv2
import video_summarizer as vidsum


def something_moves(img, threshold=250):
    global first_frame

    try:
        movement = vidsum.detect_difference(first_frame, img, threshold)
    except ValueError:
        first_frame = img
        movement = vidsum.detect_difference(first_frame, img, threshold)

    first_frame = img

    return movement


first_frame = None

input_video_path = "input_videos/original.mp4"

cap = cv2.VideoCapture(input_video_path)

if not cap.isOpened():
    print(f"[ERROR] Error opening video file {input_video_path}")

while cap.isOpened():

    ret, frame = cap.read()
    if not ret:
        break

    output_frame = frame.copy()

    if something_moves(frame):
        cv2.putText(output_frame, "Movement Detected", (5, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)

    cv2.imshow("Original Video", output_frame)

    # Press 'q' to exit
    if cv2.waitKey(2) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
