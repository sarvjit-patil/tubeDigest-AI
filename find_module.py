import sys
import importlib.util

spec = importlib.util.find_spec("youtube_transcript_api")
if spec:
    print("Found spec at:", spec.origin)
else:
    print("Could not find youtube_transcript_api")
