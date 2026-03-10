import youtube_transcript_api
import sys

print(f"Python Version: {sys.version}")
print(f"File Path: {youtube_transcript_api.__file__}")
print(f"Attributes: {dir(youtube_transcript_api)}")
try:
    from youtube_transcript_api import YouTubeTranscriptApi
    print(f"YouTubeTranscriptApi Attributes: {dir(YouTubeTranscriptApi)}")
    if hasattr(YouTubeTranscriptApi, 'get_transcript'):
        print("get_transcript found!")
    else:
        print("get_transcript NOT found!")
except Exception as e:
    print(f"Import Error: {e}")
