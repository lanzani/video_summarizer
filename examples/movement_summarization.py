import video_summarizer as vidsum

input_video_path = "input_videos/original.mp4"
output_video_path = "output_videos/video_output.mp4"

vidsum.summarize(input_video_path, output_video_path, mode="movement", movement_threshold=250)
