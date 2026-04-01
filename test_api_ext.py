from youtube_transcript_api import YouTubeTranscriptApi
import sys

def test_fetch(video_id):
    langs_to_try = ['hi', 'mr', 'en']
    try:
        print(f"Trying to get transcript for {video_id} with languages: {langs_to_try}")
        transcript_data = YouTubeTranscriptApi.get_transcript(video_id, languages=langs_to_try)
        print("Success!")
        print(transcript_data[:2])
    except Exception as e:
        print(f"Failed with requested languages: {type(e).__name__}: {str(e)}")
        try:
            print("Trying default get_transcript()...")
            transcript_data = YouTubeTranscriptApi.get_transcript(video_id)
            print("Success with default!")
            print(transcript_data[:2])
        except Exception as inner_e:
            print(f"Failed default: {type(inner_e).__name__}: {str(inner_e)}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        test_fetch(sys.argv[1])
    else:
        test_fetch("jNQXAC9IVRw") # Me at the zoo (en only)
        test_fetch("nPTcAWoQkC8") # Hindi video
