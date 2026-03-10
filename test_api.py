import sys
import youtube_transcript_api

try:
    print("Module built-ins:", dir(youtube_transcript_api))
    print("YouTubeTranscriptApi type:", type(youtube_transcript_api.YouTubeTranscriptApi))
    print("YouTubeTranscriptApi attrs:", dir(youtube_transcript_api.YouTubeTranscriptApi))
    
    # testing fetch
    res = youtube_transcript_api.YouTubeTranscriptApi.get_transcript("jNQXAC9IVRw")
    print("Fetch succeeded:", len(res))
except Exception as e:
    print("Error:", e)
