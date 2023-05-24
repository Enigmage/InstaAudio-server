from typing import Optional
import io
from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import FileResponse

from pydantic import BaseModel
from preprocessor import pdf_preprocess_text, pdf_extract_text, url_preprocess_text
from summarizer import extractive_summarizer, abstractive_summarizer
from tts import generate_audio


app = FastAPI()


@app.post("/convert-file")
async def index(file: Optional[UploadFile] = None):
    print("request received")
    if file:
        pdf_content = await file.read()
        pdf_file = io.BytesIO(pdf_content)

        filtered_text = pdf_preprocess_text(pdf_extract_text(pdf_file))

        output_path = generate_audio(abstractive_summarizer(filtered_text))

        if output_path:
            print("success")
            return FileResponse(output_path)
        raise HTTPException(
            status_code=500, detail="Output audio generation failed from document"
        )
    raise HTTPException(status_code=400, detail="No input provided")


class UrlInput(BaseModel):
    url: Optional[str] = None


@app.post("/convert-url")
def handle_input(req: UrlInput):
    print("request received")
    if req.url:
        text, formatted_text = url_preprocess_text(req.url)
        summary = extractive_summarizer(text, formatted_text)
        # summary = abstractive_summarizer(text)
        output_path = generate_audio(summary)
        if output_path:
            print("success")
            return FileResponse(output_path)
        raise HTTPException(
            status_code=500, detail="Output audio generation failed from url"
        )
    raise HTTPException(status_code=400, detail="No input provided")
