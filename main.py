from typing import Optional
from fastapi import FastAPI, UploadFile
from pydantic import BaseModel
from preprocessor import link_extractor
from semantic_extractor import nlp_summarizer


app = FastAPI()


class UserInput(BaseModel):
    link: Optional[str]
    mimetype: Optional[str]
    file: Optional[UploadFile]


@app.get("/")
def index():
    return "Hello World"


@app.post("/convert")
def handle_input(req: UserInput):
    resp = {"text": ""}
    if req.link:
        resp["text"], formatted_text = link_extractor(req.link)
        summary = nlp_summarizer(resp["text"], formatted_text)
    return resp
