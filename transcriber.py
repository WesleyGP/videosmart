import re
from youtube_transcript_api import YouTubeTranscriptApi

def extract_video_id(url: str) -> str:
    """
    Extracts the video ID from a YouTube URL.
    Supports various formats like:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    - https://www.youtube.com/shorts/VIDEO_ID
    """
    patterns = [
        r"(?:v=|\/)([0-9A-Za-z_-]{11}).*",
        r"youtu\.be\/([0-9A-Za-z_-]{11})",
        r"youtube\.com\/shorts\/([0-9A-Za-z_-]{11})"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None






import os

def get_transcript(video_id: str):
    """
    Fetches the transcript for a given video ID.
    Supports cookies.txt to bypass cloud provider IP blocks.
    """
    cookie_path = 'cookies.txt'
    
    try:
        # Check if cookies file exists
        if os.path.exists(cookie_path):
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['pt', 'en'], cookies=cookie_path)
        else:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['pt', 'en'])
        
        return transcript
    except Exception as e:
        try:
            # Fallback to default fetch
            if os.path.exists(cookie_path):
                transcript = YouTubeTranscriptApi.get_transcript(video_id, cookies=cookie_path)
            else:
                transcript = YouTubeTranscriptApi.get_transcript(video_id)
            return transcript
        except Exception as e2:
            error_msg = str(e2)
            if "cookies" in error_msg.lower():
                return {"error": "Erro com os cookies do YouTube. Tente exportar novamente."}
            if "blocked" in error_msg.lower() or "cloud provider" in error_msg.lower():
                return {"error": "O YouTube bloqueou o acesso do Render. Siga as instruções para configurar o cookies.txt."}
            return {"error": f"Não foi possível obter a transcrição: {error_msg}"}





