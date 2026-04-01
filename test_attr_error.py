import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils.youtube_helper import get_video_transcript

# MKBHD video or any other generic video
vid = "jNQXAC9IVRw" 
try:
    transcript = get_video_transcript(vid)
    print("SUCCESS:", transcript[:100] if not transcript.startswith("System Error") else transcript)
except Exception as e:
    print(f"FAILED: {e}")
