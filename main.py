from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transcriber import extract_video_id, get_transcript
from ai import analyze_text
import uvicorn

app = FastAPI()

# Enable CORS for frontend interaction
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TranscribeRequest(BaseModel):
    url: str

class AnalyzeRequest(BaseModel):
    mode: str
    text: str


@app.get("/")
async def root():
    return {"status": "YouTube Transcription API is running", "usage": "Open code.html in your browser or POST to /api/transcribe"}

@app.post("/api/transcribe")


async def transcribe(request: TranscribeRequest):
    video_id = extract_video_id(request.url)
    if not video_id:
        raise HTTPException(status_code=400, detail="URL do YouTube inválida.")
    
    transcript = get_transcript(video_id)
    
    if isinstance(transcript, dict) and "error" in transcript:
        raise HTTPException(status_code=500, detail=transcript["error"])
        
    return {
        "video_id": video_id,
        "transcript": transcript
    }

@app.post("/api/analyze")
async def analyze(request: AnalyzeRequest):
    try:
        result = analyze_text(request.mode, request.text)
        return {
            "mode": request.mode,
            "result": result
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
