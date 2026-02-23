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






def get_transcript(video_id: str):
    """
    Fetches the transcript for a given video ID.
    Returns a list of segments or an error message.
    """
    try:
        # Instantiate the API class
        api = YouTubeTranscriptApi()
        # Try preferred languages
        transcript = api.fetch(video_id, languages=['pt', 'en'])
        
        # In this version, we get a FetchedTranscript object, so we convert to raw data
        if hasattr(transcript, 'to_raw_data'):
            return transcript.to_raw_data()
        return transcript
    except Exception:
        try:
            # Fallback to default fetch
            transcript = YouTubeTranscriptApi().fetch(video_id)
            if hasattr(transcript, 'to_raw_data'):
                return transcript.to_raw_data()
            return transcript
        except Exception as e:
            return {"error": f"Não foi possível obter a transcrição: {str(e)}"}





