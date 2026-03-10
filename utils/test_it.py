from utils.youtube_helper import get_video_transcript

transcript = get_video_transcript('dQw4w9WgXcQ')
with open('test_res.txt', 'w', encoding='utf-8') as f:
    f.write(str(len(transcript)))
    f.write('\n')
    f.write(transcript[:100] if len(transcript) > 0 else transcript)
