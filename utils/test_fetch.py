import re, json, urllib.request, xml.etree.ElementTree as ET

def test_fetch(video_id):
    try:
        url = f"https://www.youtube.com/watch?v={video_id}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req).read().decode('utf-8')
        
        match = re.search(r'"captionTracks":(\[.*?\])', html)
        if not match:
             print("Error: No captions available for this video.")
             return
             
        captions = json.loads(match.group(1))
        
        if not captions:
             print("Error: Captions list is empty.")
             return
             
        target_track = None
        for track in captions:
            if 'en' in track.get('languageCode', ''):
                target_track = track
                break
        
        if not target_track:
            target_track = captions[0]
            
        xml_url = target_track['baseUrl']
        print("XML URL:", xml_url[:100], "...")
        
        # Adding some robust headers to the XML request
        req2 = urllib.request.Request(xml_url, headers={'User-Agent': 'Mozilla/5.0'})
        xml_content = urllib.request.urlopen(req2).read()
        print("XML Response Size:", len(xml_content))
        print("XML Starts With:", xml_content[:50])
        
        if not xml_content:
             print("Error: Empty XML response.")
             return
             
        root = ET.fromstring(xml_content)
        transcript = " ".join([child.text for child in root if child.text])
        print("Transcript Length:", len(transcript))
        print("Preview:", transcript[:100])
        
    except Exception as e:
        print("Exception:", str(e))

test_fetch("dQw4w9WgXcQ")
