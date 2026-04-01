import yt_dlp
import json
import urllib.request
import re

def extract_video_id(url):
    """
    Extracts the video ID from a YouTube URL.
    """
    video_id_match = re.search(r"(?<=v=)[^&#?]+", url)
    if not video_id_match:
        video_id_match = re.search(r"(?<=be/)[^&#?]+", url)
    return video_id_match.group(0) if video_id_match else None

def get_video_transcript(video_id):
    """
    Fetches the transcript of a YouTube video using youtube-transcript-api.
    Prioritizes Hindi, then Marathi, then English.
    """
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        
        # Priority 1: Hindi, Priority 2: Marathi, Priority 3: English
        langs_to_try = ['hi', 'mr', 'en']
        
        try:
            # We initialize an instance of YouTubeTranscriptApi according to the new API v0.7.0+
            ytt_api = YouTubeTranscriptApi()
            
            # This tries to fetch the transcript in the requested languages
            # It will automatically pick the first available one from the priority list
            transcript_list = ytt_api.fetch(video_id, languages=langs_to_try)
        except Exception:
            # If not found, try to list all available transcripts
            try:
                transcript_meta = ytt_api.list(video_id)
                # First try to find a generated one in our languages
                found_transcript = None
                
                # Try to find exactly one of our preferred languages
                for lang_code in langs_to_try:
                    try:
                        found_transcript = transcript_meta.find_transcript([lang_code])
                        break
                    except Exception:
                        pass
                
                # If still not found, just grab whichever generated or manual transcript exists, 
                # then try to translate it to English or Hindi if possible, otherwise just use it
                if not found_transcript:
                    try:
                        # Grab any available transcript
                        found_transcript = transcript_meta.find_generated_transcript(['en'])
                    except Exception:
                        # Grab whatever is available
                        transcript_meta_list = list(transcript_meta)
                        if transcript_meta_list:
                            found_transcript = transcript_meta_list[0]
                
                if found_transcript:
                    # Translate to English if it's not and we have no other choice
                    if not found_transcript.language_code.startswith('en') and \
                       not found_transcript.language_code.startswith('hi') and \
                       not found_transcript.language_code.startswith('mr'):
                        try:
                           found_transcript = found_transcript.translate('en')
                        except Exception:
                           pass
                    transcript_list = found_transcript.fetch()
                else:
                     available_langs = []
                     try:
                         for t in transcript_meta:
                             available_langs.append(t.language_code)
                         return f"System Error: No suitable subtitles found. Available subtitles: {available_langs}"
                     except AttributeError:
                         return "System Error: No suitable subtitles found for this video."

            except Exception as inner_e:
                print(f"Fallback Error finding transcripts: {inner_e}")
                import traceback
                
                # Check for specific youtube_transcript_api errors
                error_msg = str(inner_e)
                if "TranscriptsDisabled" in str(type(inner_e)):
                    return "System Error: The creator has disabled subtitles for this video."
                elif "NoTranscriptAvailable" in str(type(inner_e)):
                    return "System Error: No subtitles are available for this video."
                elif "VideoUnavailable" in str(type(inner_e)):
                    return "System Error: The video is unavailable or private."
                else:
                    return f"System Error: Could not retrieve transcript. Reason: {type(inner_e).__name__}.\nDetails: {traceback.format_exc()}"
                
        # Join all the text pieces
        transcript_text = " ".join([item.text for item in transcript_list])
        return transcript_text if transcript_text.strip() else "System Error: Extracted transcript was empty."
        
    except Exception as e:
        import traceback
        return f"System Error during transcript fetch: {str(e)}\n{traceback.format_exc()}"

def get_video_thumbnail_url(video_id):
    """
    Returns the URL for the video's high-quality thumbnail.
    Using hqdefault.jpg as it is guaranteed to exist for all videos,
    unlike maxresdefault.jpg which is often missing.
    """
    return f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
