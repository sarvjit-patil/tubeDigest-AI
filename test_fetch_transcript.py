import sys
import traceback
from utils.youtube_helper import get_video_transcript

video_id = "jNQXAC9IVRw"

try:
    transcript = get_video_transcript(video_id)
    with open("test_out_verify.txt", "w", encoding="utf-8") as f:
        f.write("Success. Transcript:\n")
        f.write(transcript[:500] + "...")
except Exception as e:
    with open("test_out_verify.txt", "w", encoding="utf-8") as f:
        f.write(f"Exception: {e}\n")
        f.write(traceback.format_exc())
