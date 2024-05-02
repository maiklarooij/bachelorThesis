import json
import os
import torch

import warnings

from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse

from appUtils import (
    verify_whisper_return_code,
    verify_pyannote_return_code,
    get_number_videos_gemeentes,
    get_video_length,
)
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

warnings.filterwarnings("ignore")

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
print("Loading pyannote client")
pyannote_client = Pyannote(device)

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


app.mount(
    "/videos",
    StaticFiles(directory="/Users/personal/Desktop/scriptie/notebooks/data"),
    name="videos",
)


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

    kwargs = {
        "collection": body.collection,
        "query": body.query,
        "vector": body.vector,
        "limit": body.limit,
        "alpha": body.alpha,
        "governments": body.government,
        "meeting_types": body.meetingType,
        "years": body.year,
        "speakers": body.speaker,
        "videos": body.video,
    }
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

    kwargs = {
        "collection": body.collection,
        "query": body.query,
        "limit": body.limit,
        "governments": body.government,
        "meeting_types": body.meetingType,
        "years": body.year,
        "speakers": body.speaker,
        "videos": body.video,
    }
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

    objects = weaviate_client.search_vector(
        body.collection,
        body.vector,
        body.limit,
        body.government,
        body.meetingType,
        body.year,
        body.speaker,
        body.video,
    )
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


BASE_PATHS = [
    "/Volumes/Samsung_T5/data/",
    "/Volumes/Drive/data/",
    # "/Users/personal/Desktop/scriptie/notebooks/data/",
]
@app.get("/api/gemeentes")
async def get_gemeentes():
    gemeentes = []
    for path in BASE_PATHS:
        gemeentes += [os.path.join(path, gems) for gems in os.listdir(path)]

    gemeentes = [
        {
            "gemeente": g.split("/")[-1],
            "videos": get_number_videos_gemeentes(g),
            "path": g,
        }
        for g in gemeentes
        if not g.split("/")[-1].startswith(".")
    ]

    return { "status": "OK", "gemeentes": gemeentes}


@app.get("/api/gemeenteMeetingTypes")
async def get_gemeente_types(gemeente: str):
    p = None
    for path in BASE_PATHS:
        if os.path.isdir(f"{path}/{gemeente}"):
            p = f"{path}/{gemeente}"
    if not p:
        raise HTTPException(
            status_code=404, detail=f"Gemeente {gemeente} does not exist."
        )

    meetingTypes = [
        {
            "type": t,
        }
        for t in os.listdir(p)
        if not t.startswith(".")
    ]

    return {"status": "OK", "types": meetingTypes}


@app.get("/api/gemeenteYears")
async def get_gemeente_years(gemeente: str, meetingType: str):
    p = None
    # Gets meeting
    for path in BASE_PATHS:
        if os.path.isdir(f"{path}/{gemeente}/{meetingType}"):
            p = f"{path}/{gemeente}/{meetingType}"
    if not p:
        raise HTTPException(
            status_code=404,
            detail=f"Gemeente {gemeente} with type {meetingType} does not exist.",
        )

    years = [
        {"year": y}
        for y in os.listdir(p)
        if not y.startswith(".")
    ]

    return {"status": "OK", "years": years}

@app.get("/api/getVideos")
async def get_gemeente_videos(gemeente: str, meetingType: str, year: str):
    p = None
    # Gets meeting
    for path in BASE_PATHS:
        if os.path.isdir(f"{path}/{gemeente}/{meetingType}/{year}"):
            p = f"{path}/{gemeente}/{meetingType}/{year}"
    if not p:
        raise HTTPException(
            status_code=404,
            detail=f"Gemeente {gemeente} with type {meetingType} and year {year} does not exist.",
        )

    video_dir = f"{p}/videos"
    if os.path.isdir(video_dir):
        videos = [
            {"video": v.replace(".mp4", "")}
            for v in os.listdir(video_dir)
            if not v.startswith(".")
        ]
    else:
        print("No videos directory exists", video_dir)
        videos = []

    return {"status": "OK", "videos": videos}


@app.get("/api/getVideoData")
async def get_gemeente_video_data(gemeente: str, meetingType: str, year: str, video: str):
    p = None
    for path in BASE_PATHS:
        if os.path.isfile(f"{path}/{gemeente}/{meetingType}/{year}/videos/{video}"):
            p = f"{path}/{gemeente}/{meetingType}/{year}/videos/{video}"
    if not p:
        raise HTTPException(
            status_code=404,
            detail=f"video {video} with gemeente {gemeente} with type {meetingType} and year {year} does not exist.",
        )
    duration = get_video_length(p)
    print(os.path.abspath(p))
    return {"status": "OK", "duration": duration}

@app.get("/api/getVideo")
async def get_gemeente_video(gemeente: str, meetingType: str, year: str, video: str):
    p = None
    for path in BASE_PATHS:
        if os.path.isfile(f"{path}/{gemeente}/{meetingType}/{year}/videos/{video}"):
            p = f"{path}/{gemeente}/{meetingType}/{year}/videos/{video}"
    if not p:
        raise HTTPException(
            status_code=404,
            detail=f"video {video} with gemeente {gemeente} with type {meetingType} and year {year} does not exist.",
        )

    print(os.path.abspath(p))

    return FileResponse(os.path.abspath(p), media_type="video/mp4")


@app.get("/api/getAgenda")
async def get_video_agenda(gemeente: str, meetingType: str, year: str, video: str):
    video = video.replace(".mp4", "")
    p = None
    for path in BASE_PATHS:
        if os.path.isfile(f"{path}/{gemeente}/{meetingType}/{year}/agendas/{video}.json"):
            p = f"{path}/{gemeente}/{meetingType}/{year}/agendas/{video}.json"
    if not p:
        raise HTTPException(
            status_code=404,
            detail=f"agenda for video {video} with gemeente {gemeente} with type {meetingType} and year {year} does not exist.",
        )

    with open(p, "r") as f:
        agenda_data = json.load(f)

    return {"status": "OK", "agenda": agenda_data}


@app.get("/api/getSpeakers")
async def get_video_speakers(gemeente: str, meetingType: str, year: str, video: str):
    p = None
    for path in BASE_PATHS:
        if os.path.isfile(f"{path}/{gemeente}/{meetingType}/{year}/turnObjects/{video}.json"):
            p = f"{path}/{gemeente}/{meetingType}/{year}/turnObjects/{video}.json"
    if not p:
        raise HTTPException(
            status_code=404,
            detail=f"speakers for video {video} with gemeente {gemeente} with type {meetingType} and year {year} do not exist.",
        )

    with open(p, "r") as f:
        speakers = json.load(f)

    speakers_shortened = [
        {"speaker": s["speaker"], "start": s["start"], "end": s["end"]}
        for s in speakers
    ]

    return {"status": "OK", "speakers": speakers_shortened}

@app.get("/api/getTranscript")
async def get_video_transcript(gemeente: str, meetingType: str, year: str, video: str):
    p = None
    for path in BASE_PATHS:
        if os.path.isfile(f"{path}/{gemeente}/{meetingType}/{year}/videos/{video}"):
            p = f"{path}/{gemeente}/{meetingType}/{year}/videos/{video}"
    if not p:
        raise HTTPException(
            status_code=404,
            detail=f"video {video} with gemeente {gemeente} with type {meetingType} and year {year} does not exist.",
        )

    transcript_path = f"{path}/{gemeente}/{meetingType}/{year}/transcripts/{video}.json"
    if not os.path.isfile(transcript_path):
        raise HTTPException(
            status_code=404,
            detail=f"Transcript for video {video} with gemeente {gemeente} with type {meetingType} and year {year} does not exist.",
        )

    with open(transcript_path, "r") as f:
        data = json.load(f)

    transcript = data.get("text")

    return {"status": "OK", "transcript": transcript}
