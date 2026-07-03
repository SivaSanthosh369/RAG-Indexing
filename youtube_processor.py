# youtube_processor.py
from youtube_transcript_api import YouTubeTranscriptApi
import re

def extract_video_id(url):
    """Extracts the video ID from a YouTube URL."""
    pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    match = re.search(pattern, url)
    return match.group(1) if match else None

def extract_and_chunk_youtube(url):
    """Extracts and chunks a YouTube transcript (ADHD-Friendly)"""
    video_id = extract_video_id(url)
    if not video_id:
        return None
        
    try:
        # transcript = YouTubeTranscriptApi.get_trans
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'ml'])
        
        chunks_with_time = []
        current_chunk = ""
        start_time = 0
        
        for entry in transcript:
            sentence = entry['text']
            if len(current_chunk) == 0:
                start_time = int(entry['start'])
                
            if len(current_chunk) + len(sentence) < 400:
                current_chunk += " " + sentence
            else:
                # Calculate timestamp for the chunk
                minutes = start_time // 60
                seconds = start_time % 60
                timestamp = f"{minutes:02d}:{seconds:02d}"
                
                chunks_with_time.append({
                    "text": current_chunk.strip(),
                    "page": f"Timestamp {timestamp}" # Calculate timestamp for the chunk
                })
                current_chunk = sentence
                start_time = int(entry['start'])
                
        if current_chunk.strip():
            minutes = start_time // 60
            seconds = start_time % 60
            chunks_with_time.append({
                "text": current_chunk.strip(),
                "page": f"Timestamp {minutes:02d}:{seconds:02d}"
            })
            
        return chunks_with_time
    except Exception as e:
        print(f"YouTube Error: {e}")
        return None