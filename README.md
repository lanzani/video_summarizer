# Video Summarizer

---

A time saver tool that transform long footage in a short video keeping the meaningful parts. 
Useful to compress video surveillance footage.

## Installation

---
Use `pip install video_summarizer`.


## Features / Usage

---

### Video Summarization

#### Motion summarization
**Usage:**
```python
import video_summarizer as vidsum

input_video_path = "input_videos/original.mp4"
output_video_path = "output_videos/processed.mp4"

vidsum.summarize(input_video_path, output_video_path, mode="motion")

```

### Movement Detector
... Work in progress ...

### Heatmap
... Work in progress ...