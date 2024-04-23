import argparse
import os

import torch

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

from appUtils import verify_whisper_return_code
from UserTypes import TranscribeBody
from WhisperClient import MLX_Transcriber, Torch_Transcriber

load_dotenv()

device = "mps" if torch.backends.mps.is_available() else 'cuda' if torch.cuda.is_available() else "cpu"
print(f"Running on {device}")

def parse_args():
    parser = argparse.ArgumentParser(description="Woogle video archive search backend.")
    parser.add_argument("-w", "--whisper", action="store_true")
    parser.add_argument("-v", "--weaviate", action="store_true")
    parser.add_argument("-p", "--pyannote", action="store_true")
    parser.add_argument("-e", "--embed", action="store_true")
    parser.add_argument("-l", "--llm", action="store_true")

    return parser.parse_args()


# TODO: check if cuda/ mlx is available and initialise based on that
whisper_client = None
if device == "mps":
    print("Loading whisper MLX client")
    whisper_client = MLX_Transcriber(os.environ.get("MLX_WHISPER_MODEL"))
else:
    print("Loading whisper Torch client")
    whisper_client = Torch_Transcriber()
transcribing = False

print("Loading pyannote client")
pyannote_client = Pyannote(device)

print("Loading Weaviate client")
weaviate_client = Weaviate()

print("Loading embedding client")
embed_client = SFRMistralEmbedder()

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
@app.post("/api/pyannote/diorize")
async def diorize(body: DiorizeBody):
    if not pyannote_client:
        raise HTTPException(status_code=503, detail="Pyannote client not active")

    try:
        r = pyannote_client.diorize(body.input_path, body.output_path)
    except Exception as e:
        print("Error in pyannote diorization:", e)
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

    verify_pyannote_return_code(r)

    return { "status": "OK" }


@app.post("/api/pyannote/embed")
async def embed_speech(body: SpeechEmbedBody):
    if not pyannote_client:
        raise HTTPException(status_code=503, detail="Pyannote client not active")

    try:
        embedding = pyannote_client.embed(body.input_path, body.output_path, body.from_time, body.to_time)
    except Exception as e:
        print("Error embedding!", e)
        embedding = None

    # verify_pyannote_return_code(r)
    # embedding = None # todo

    try:
        return { "status": "OK", "embedding": embedding }
    except Exception as e:
        print("Error serializing:", e)
        return { "status": "OK", "embedding": None }


# TODO: error handling
@app.get("/api/weaviate/getInfo")
async def get_info():
    if not weaviate_client:
        raise HTTPException(status_code=503, detail="Weaviate client not active")

    info = weaviate_client.get_info()
    return { "status": "OK", "info": info }


# TODO: error handling
@app.get("/api/weaviate/getCollections")
async def get_colletions():
    if not weaviate_client:
        raise HTTPException(status_code=503, detail="Weaviate client not active")

    collections = weaviate_client.get_all_collections()
    print(collections)

    return { "status": "OK", "collections": collections } # TODO: Return collections


# TODO: error handling
@app.get("/api/weaviate/getCollection")
async def get_colletion():
    if not weaviate_client:
        raise HTTPException(status_code=503, detail="Weaviate client not active")

    info = weaviate_client.get_collection_info("TestCollection")
    print(info)

    return { "status": "OK", "collectionInfo": info }

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
async def embed(body: EmbedBody):
    if not embed_client:
        raise HTTPException(status_code=503, detail="Text embed client not active")

    embeddings = embed_client.embed(body.text).tolist()

    return { "status": "OK", "embeddings": embeddings }
