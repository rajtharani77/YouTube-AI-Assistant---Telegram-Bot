from fastapi import FastAPI
from services.youtube_service import process_youtube_video
from core.summarizer import generate_summary

app = FastAPI(title="YouTube AI Assistant")


@app.get("/")
def health():
    return {"status": "running"}


@app.post("/summarize")
def summarize(url: str):

    video = process_youtube_video(url)
    summary = generate_summary(video["text"])

    return {"summary": summary}