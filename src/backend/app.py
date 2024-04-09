import os

import torch

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

from appUtils import verify_whisper_return_code
from UserTypes import TranscribeBody
from WhisperClient import MLX_Transcriber, Torch_Transcriber

load_dotenv()

# TODO: check if cuda/ mlx is available and initialise based on that
whisper_client = None
if torch.backends.mps.is_available():
    whisper_client = MLX_Transcriber(os.environ.get("MLX_WHISPER_MODEL"))
else:
    whisper_client = Torch_Transcriber()
transcribing = False

weaviate_client = None
embed_client = None
pyannote_client = None

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "OK"}


@app.post("/api/whisper/transcribe")
async def transcribe(body: TranscribeBody):
    global transcribing
    if transcribing:
        raise HTTPException(status_code=503, detail="Whisper client is busy")

    transcribing = True
    try:
        r = whisper_client.transcribe(body.input_path, body.output_path)
    except Exception as _:
        transcribing = False

    verify_whisper_return_code(r)
    transcribing = False

    return {"status": "OK"}


# TODO
@app.get("/api/whisper/load")
async def load_transcription():
    raise HTTPException(status_code=501, detail="Not implemented")


# TODO
@app.post("/api/weaviate/createCollection")
async def create_collection():
    raise HTTPException(status_code=501, detail="Not implemented")

# TODO
@app.post("/api/weaviate/insert")
async def insert():
    raise HTTPException(status_code=501, detail="Not implemented")

# TODO
@app.get("/api/weaviate/search")
async def search():
    raise HTTPException(status_code=501, detail="Not implemented")

# TODO
@app.post("/api/weaviate/deleteCollection")
async def delete_collection():
    raise HTTPException(status_code=501, detail="Not implemented")

# TODO
@app.post("/api/weaviate/deleteEntry")
async def delete_entry():
    raise HTTPException(status_code=501, detail="Not implemented")


# TODO
@app.post("/api/embed")
async def embed():
    raise HTTPException(status_code=501, detail="Not implemented")
