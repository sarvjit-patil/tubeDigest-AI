import sys
import importlib

print("Python Path:", sys.path)

try:
    import youtube_transcript_api
    print("\n--- Module info ---")
    print("File:", getattr(youtube_transcript_api, '__file__', 'N/A'))
    print("Dir contents:", dir(youtube_transcript_api))
except Exception as e:
    print(e)
