import urllib.request, re, json, xml.etree.ElementTree as ET

def test_fetch(video_id):
    try:
        url = f"https://www.youtube.com/watch?v={video_id}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req).read().decode('utf-8')
        
        match = re.search(r'"captionTracks":(\[.*?\])', html)
        if not match:
             return "Error: No captions available for this video."
             
        captions = json.loads(match.group(1))
        
        if not captions:
             return "Error: Captions list is empty."
             
        target_track = None
        for track in captions:
            if 'en' in track.get('languageCode', ''):
                target_track = track
                break
        
        if not target_track:
            target_track = captions[0]
            
        base_url = target_track['baseUrl']
        if 'fmt=' not in base_url:
            base_url += '&fmt=json3' if '?' in base_url else '?fmt=json3'
            
        req2 = urllib.request.Request(base_url, headers={'User-Agent': 'Mozilla/5.0'})
        raw_content = urllib.request.urlopen(req2).read()
        
        try:
            caption_data = json.loads(raw_content.decode('utf-8'))
            events = caption_data.get('events', [])
            transcript = " ".join([seg.get('utf8', '') for event in events for seg in event.get('segs', []) if seg.get('utf8', '').strip()])
            if transcript:
                return transcript
        except Exception as json_e:
            pass
            
        root = ET.fromstring(raw_content)
        transcript = " ".join([child.text for child in root if child.text])
        return transcript
        
    except Exception as e:
        return f"System Error during custom transcript fetch: {str(e)}"

result = test_fetch("dQw4w9WgXcQ")
with open("d:\\Project\\tubeDigest-AI\\debug_transcript.txt", "w", encoding="utf-8") as f:
    f.write(result)
