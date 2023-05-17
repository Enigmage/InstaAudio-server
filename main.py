from typing import Optional
from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel
from preprocessor import link_extractor
from semantic_extractor import nlp_summarizer
from tts import generate_audio


app = FastAPI()


class UserInput(BaseModel):
    link: Optional[str]
    file: Optional[UploadFile]


@app.get("/")
def index():
    return "Hello World"


@app.post("/convert")
def handle_input(req: UserInput):
    if not req.link and not req.file:
        raise HTTPException(status_code=400, detail="No input provided")
    if req.link:
        text, formatted_text = link_extractor(req.link)
        summary = nlp_summarizer(text, formatted_text)
        output_path = generate_audio(summary)
        if output_path:
            return FileResponse(output_path)
        raise HTTPException(
            status_code=500, detail="Output audio generation failed from url"
        )
