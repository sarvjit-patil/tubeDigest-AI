import yt_dlp
import json
import urllib.request

video_id = "jNQXAC9IVRw"
url = f"https://www.youtube.com/watch?v={video_id}"

ydl_opts = {
    'skip_download': True,
    'writesubtitles': True,
    'writeautomaticsub': True,
    'subtitleslangs': ['en'],
    'quiet': True,
}

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
            print("No english subs found.")
        else:
            json3_url = None
            for fmt in target_sub:
                if fmt.get('ext') == 'json3':
                    json3_url = fmt.get('url')
                    break
                    
            if json3_url:
                req = urllib.request.Request(json3_url, headers={'User-Agent': 'Mozilla/5.0'})
                resp = urllib.request.urlopen(req).read().decode('utf-8')
                data = json.loads(resp)
                events = data.get('events', [])
                transcript = " ".join([seg.get('utf8', '') for event in events for seg in event.get('segs', []) if seg.get('utf8', '').strip()])
                print("SUCCESS:", transcript[:200])
            else:
                print("JSON3 not found.")
except Exception as e:
    print("ERROR:", e)
