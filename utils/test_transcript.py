import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.youtube_helper import get_video_transcript
res = get_video_transcript('dQw4w9WgXcQ')
print(res[:100] if res else 'None')
