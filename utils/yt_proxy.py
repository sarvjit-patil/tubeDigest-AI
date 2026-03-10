import sys
import json
import urllib.request
import re
import xml.etree.ElementTree as ET

def fetch_transcript(video_id):
    try:
        url = f"https://www.youtube.com/watch?v={video_id}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req).read().decode('utf-8')
        
        # Extract the caption tracks JSON
        match = re.search(r'"captionTracks":(\[.*?\])', html)
        if not match:
             return {"error": "No captions available for this video."}
             
        captions = json.loads(match.group(1))
        
        if not captions:
             return {"error": "Captions list is empty."}
             
        # Find English or fallback to first
        target_track = None
        for track in captions:
            if 'en' in track.get('languageCode', ''):
                target_track = track
                break
        
        if not target_track:
            target_track = captions[0]
            
        xml_url = target_track['baseUrl']
        xml_content = urllib.request.urlopen(xml_url).read()
        
        # Parse XML to text
        root = ET.fromstring(xml_content)
        transcript = " ".join([child.text for child in root if child.text])
        return {"success": True, "transcript": transcript}
        
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(json.dumps(fetch_transcript(sys.argv[1])))
    else:
        print(json.dumps({"error": "No video ID provided"}))
