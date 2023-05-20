from typing import Optional
import io
import PyPDF2
from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import FileResponse

from pydantic import BaseModel
from preprocessor import link_extractor
from preprocessor import preprocess_text
from summarizer import nlp_summarizer
from tts import generate_audio


app = FastAPI()


@app.post("/convert-file")
async def index(file: Optional[UploadFile] = None):
    print("request")
    if file:
        # print("In")
        pdf_content = await file.read()
        pdf_file = io.BytesIO(pdf_content)

        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

        filtered_text = preprocess_text(text)

        output_path = generate_audio(filtered_text)

        if output_path:
            print("Complete")
            return FileResponse(output_path)
        raise HTTPException(
            status_code=500, detail="Output audio generation failed from document"
        )
    raise HTTPException(status_code=400, detail="No input provided")


class UrlInput(BaseModel):
    url: Optional[str] = None


@app.post("/convert-url")
def handle_input(req: UrlInput):
    print("request")
    if req.url:
        text, formatted_text = link_extractor(req.url)
        summary = nlp_summarizer(text, formatted_text)
        output_path = generate_audio(summary)
        if output_path:
            print("Complete")
            return FileResponse(output_path)
        raise HTTPException(
            status_code=500, detail="Output audio generation failed from url"
        )
    raise HTTPException(status_code=400, detail="No input provided")
