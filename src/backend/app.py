import os
import torch

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

from appUtils import verify_whisper_return_code, verify_pyannote_return_code
from UserTypes import (
    TranscribeBody,
    DiorizeBody,
    SpeechEmbedBody,
    WeaviateCreateCollectionBody,
    WeaviateGetCollectionBody,
    WeaviateInsertBody,
    EmbedBody,
    WeaviateSearchHybridBody,
    WeaviateSearchBM25Body,
    WeaviateSearchVectorBody,
    WeaviateDeleteCollectionBody,
    AgendaBody,
    WhisperReturnCodes,
)

from WhisperClient import MLX_Transcriber, Torch_Transcriber
from PyannoteClient import Pyannote
from WeaviateClient import Weaviate
from EmbedClient import SFRMistralEmbedder, MpnetEmbedder
from LlmClient import MlxLlama

load_dotenv()

device = "mps" if torch.backends.mps.is_available() else 'cuda' if torch.cuda.is_available() else "cpu"
print(f"Running on {device}")

# TODO: check if cuda/ mlx is available and initialise based on that
whisper_client = None
# if device == "mps":
#     print("Loading whisper MLX client")
#     whisper_client = MLX_Transcriber(os.environ.get("MLX_WHISPER_MODEL"))
# else:
#     print("Loading whisper Torch client")
#     whisper_client = Torch_Transcriber()

pyannote_client = None
# print("Loading pyannote client")
# pyannote_client = Pyannote(device)

weaviate_client = None
# print("Loading Weaviate client")
# weaviate_client = Weaviate()

embed_client = None
# print("Loading embedding client")
# embed_client = MpnetEmbedder()

llm_client = None
# print("Loading llm client")
# llm_client = MlxLlama(model_name="mlx-community/Meta-Llama-3-8B-Instruct-8bit")

app = FastAPI()

@app.get("/api/status")
async def root():
    return { "status": "OK" }


@app.post("/api/whisper/transcribe")
async def transcribe(body: TranscribeBody):
    if not whisper_client:
        raise HTTPException(status_code=503, detail="Whisper client not active")

    try:
        r = whisper_client.transcribe(body.input_path, body.output_path)
    except Exception as e:
        print("Error!", e)
        r = WhisperReturnCodes.OTHER_ERROR

    verify_whisper_return_code(r)

    return { "status": "OK" }


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
        embedding = pyannote_client.embed(body.input_path, body.from_time, body.to_time)
    except Exception as e:
        print("Error in pyannote embedding!", e)
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

    try:
        return { "status": "OK", "embedding": embedding }
    except Exception as e:
        print("Error serializing:", e)
        HTTPException(status_code=500, detail=f"Internal server error: {e}")


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
    # print(collections)

    return { "status": "OK", "collections": collections }


# TODO: error handling
@app.post("/api/weaviate/getCollection")
async def get_colletion(body: WeaviateGetCollectionBody):
    if not weaviate_client:
        raise HTTPException(status_code=503, detail="Weaviate client not active")

    info = weaviate_client.get_collection_info(body.collection)
    # print(info)

    return { "status": "OK", "collectionInfo": info }


# TODO: error handling
@app.post("/api/weaviate/createCollection")
async def create_collection(body: WeaviateCreateCollectionBody):
    if not weaviate_client:
        raise HTTPException(status_code=503, detail="Weaviate client not active")

    weaviate_client.create_collection(body)

    return { "status": "OK" }


# TODO: error handling
@app.post("/api/weaviate/insert")
async def insert(body: WeaviateInsertBody):
    if not weaviate_client:
        raise HTTPException(status_code=503, detail="Weaviate client not active")

    try:
        weaviate_client.insert_objects(body.collection, body.objects)
    except Exception as e:
        print("Error:", e)

    return { "status": "OK" }


# TODO: error handling
@app.post("/api/weaviate/searchHybrid")
async def search_h(body: WeaviateSearchHybridBody):
    if not weaviate_client:
        raise HTTPException(status_code=503, detail="Weaviate client not active")

    kwargs = {"collection": body.collection, "query": body.query, "vector": body.vector, "limit": body.limit, "alpha": body.alpha}
    if body.query_properties is not None:
        kwargs["query_properties"] = body.query_properties
    objects = weaviate_client.search_hybrid(**kwargs)
    # Verify objects & get return code

    return {"status": "OK", "objects": objects}


# TODO: error handling
@app.post("/api/weaviate/searchBM25")
async def search_b(body: WeaviateSearchBM25Body):
    if not weaviate_client:
        raise HTTPException(status_code=503, detail="Weaviate client not active")

    kwargs = {"collection": body.collection, "query": body.query, "limit": body.limit}
    if body.query_properties is not None:
        kwargs["query_properties"] = body.query_properties
    objects = weaviate_client.search_bm25(**kwargs)
    # Verify objects & get return code

    return {"status": "OK", "objects": objects}


# TODO: error handling
@app.post("/api/weaviate/searchVector")
async def search_v(body: WeaviateSearchVectorBody):
    if not weaviate_client:
        raise HTTPException(status_code=503, detail="Weaviate client not active")

    objects = weaviate_client.search_vector(body.collection, body.vector, body.limit)
    # Verify objects & get return code

    return { "status": "OK", "objects": objects }


# TODO: error handling
@app.post("/api/weaviate/deleteCollection")
async def delete_collection(body: WeaviateDeleteCollectionBody):
    if not weaviate_client:
        raise HTTPException(status_code=503, detail="Weaviate client not active")

    weaviate_client.delete_collection(body.collection)

    return { "status": "OK" }


# TODO: error handling
@app.post("/api/weaviate/deleteEntry")
async def delete_entry():
    if not weaviate_client:
        raise HTTPException(status_code=503, detail="Weaviate client not active")

    raise HTTPException(status_code=501, detail="Not implemented")


# TODO
@app.post("/api/embed")
async def embed(body: EmbedBody):
    if not embed_client:
        raise HTTPException(status_code=503, detail="Text embed client not active")

    embeddings = embed_client.embed(body.text).tolist()

    return { "status": "OK", "embeddings": embeddings }

@app.post("/api/agenda")
async def agenda(body: AgendaBody):
    if not llm_client:
        raise HTTPException(status_code=503, detail="Llm client not active")

    # TODO Split body.full_text in 6k token windows (with a bit of overlap)
    agenda_points = [p["agendaPoint"] for p in body.agenda_points]
    prompt = "Gegeven het volgende transcript van een gemeente vergadering en een lijst met agenda punten, per agenda punt aan bij welke zin ze beginnen. De tekst is opgedeeld in kleinere stukken, dus niet alle agenda punten hoeven aan bod te komen."


@app.post("/api/chat")
# Body should contain new question, system prompt and history of previous qa's
async def chat():
    if not llm_client:
        raise HTTPException(status_code=503, detail="Llm client not active")


BASE_PATH = "/Volumes/Samsung_T5/data/"
@app.get("/api/gemeentes")
async def get_gemeentes():
    gemeentes = os.listdir(BASE_PATH)

    return { "status": "OK", "gemeentes": gemeentes}


@app.get("/api/gemeenteVideos")
async def get_gemeente_videos(gemeente: str):
    if not os.isdir(f"{BASE_PATH}/{gemeente}"):
        raise HTTPException(status_code=500, detail=f"Gemeente {gemeente} does not exist.")

    meetings = os.listdir(f"{BASE_PATH}/{gemeente}")

    return {"status": "OK", "meetings": meetings}
