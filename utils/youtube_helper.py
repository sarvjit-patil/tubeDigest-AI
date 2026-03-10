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
    Fetches the transcript of a YouTube video using yt-dlp.
    """
    ydl_opts = {
        'skip_download': True,
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': ['en'],
        'quiet': True,
    }
    
    url = f"https://www.youtube.com/watch?v={video_id}"
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            subs = info.get('subtitles', {})
            auto_subs = info.get('automatic_captions', {})
            
            target_sub = None
            if 'en' in subs:
                target_sub = subs['en']
            elif 'en' in auto_subs:
                target_sub = auto_subs['en']
                
            if not target_sub:
                return "System Error: No English subtitles found for this video."
                
            json3_url = None
            for fmt in target_sub:
                if fmt.get('ext') == 'json3':
                    json3_url = fmt.get('url')
                    break
                    
            if not json3_url:
                if target_sub:
                   return "System Error: Subtitles are available but not in an easily parseable format via yt-dlp currently."
                return "System Error: Could not extract specific subtitle URL."
                
            req = urllib.request.Request(json3_url, headers={'User-Agent': 'Mozilla/5.0'})
            resp = urllib.request.urlopen(req).read().decode('utf-8')
            
            data = json.loads(resp)
            events = data.get('events', [])
            transcript = " ".join([seg.get('utf8', '') for event in events for seg in event.get('segs', []) if seg.get('utf8', '').strip()])
            
            return transcript if transcript else "System Error: Extracted transcript was empty."
            
    except Exception as e:
        return f"System Error during yt-dlp fetch: {str(e)}"

def get_video_thumbnail_url(video_id):
    """
    Returns the URL for the video's high-quality thumbnail.
    Using hqdefault.jpg as it is guaranteed to exist for all videos,
    unlike maxresdefault.jpg which is often missing.
    """
    return f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
