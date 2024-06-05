import json
import os
import requests
import pandas as pd

HOST = "http://localhost"
PORT = "3012"
WEAVIATE_ENDPOINT = f"{HOST}:{PORT}/api/weaviate"

def delete_collection(name):
    requests.post(
        f"{WEAVIATE_ENDPOINT}/deleteCollection", json={"collection": name}
    )


def create_speaker_collection():
    requests.post(
        f"{WEAVIATE_ENDPOINT}/createCollection",
        json={
            "name": "Speakers",
            "vector_index_hnsw": True,
            "distance_config": "cosine",
            "properties": [
                {"name": "government", "data_type": "text"},
                {"name": "name", "data_type": "text"},
            ],
        },
    )


def create_transcript_collection():
    requests.post(
        f"{WEAVIATE_ENDPOINT}/createCollectionTranscripts",
        json={
            "name": "TranscriptsV2",
            "vector_index_hnsw": True,
            "distance_config": "cosine",
            "properties": [
                {"name": "text", "data_type": "text"},
                {"name": "start", "data_type": "number"},
                {"name": "end", "data_type": "number"},
                {"name": "code", "data_type": "text"},
                {"name": "year", "data_type": "text"},
                {"name": "government", "data_type": "text"},
                {"name": "type", "data_type": "text"},
                {"name": "speaker", "data_type": "text"},
            ],
        },
    )


def add_transcripts(BASE_PATH_INIT):
    for meeting_type in os.listdir(BASE_PATH_INIT):
        if meeting_type.startswith("."):
            continue
        BASE_PATH = f"{BASE_PATH_INIT}/{meeting_type}"
        for year in os.listdir(BASE_PATH):
            if year.startswith("."):
                continue
            if not os.path.isdir(f"{BASE_PATH}/{year}") or not os.path.isdir(
                f"{BASE_PATH}/{year}/finalObjects"
            ):
                continue
            for meeting in os.listdir(f"{BASE_PATH}/{year}/finalObjects"):
                with open(f"{BASE_PATH}/{year}/finalObjects/{meeting}", "r") as fof:
                    try:
                        objects_with_embedding = json.load(fof)
                    except Exception as e:
                        print(f"Error at: {meeting}", e)
                        continue
                    requests.post(
                        f"{WEAVIATE_ENDPOINT}/insert",
                        json={
                            "collection": "TranscriptsV2",
                            "objects": objects_with_embedding,
                        },
                    )

def get_speaker_embedding(basepath, government, meeting_type, year, code, speakerID):
    path = f"{basepath}/finalObjects/{code}.mp4.json"
    with open(path, "r") as f:
        data = json.load(f)

    for d in data:
        if d["object"]["speaker"] == speakerID:
            return d["vector"]["speaker"]

    print(f"ERROR! Could not find speakerID in video {code}")

def add_weaviate(government, name, embedding):
    r = requests.post(
        f"{WEAVIATE_ENDPOINT}/insert",
        json={
            "collection": "Speakers",
            "objects": [
                {
                    "object": {"government": government, "name": name},
                    "vector": embedding,
                }
            ],
        },
    )

    if r.status_code != 200:
        print(f"ERROR INSERTING {name}!")
        return
    print(f"Inserted {name} in weaviate")

def handle_file(government, meeting_type, year, path):
    code = path.split("/")[-1].split(".")[0]
    data = pd.read_excel(path)
    done = []
    for index, row in data.iterrows():
        name = row["Naam"]
        speakerID = row["sprekerID"]
        # If speaker is named
        if not pd.isna(name) and speakerID not in done:
            if name.strip().lower() == "inspreker":
                continue
            print(
                f"{path}, Row {index+1}: 'Naam' is not empty and its value is '{name}', '{speakerID}', {code}"
            )
            p = path.split("/sheets")[0]
            embedding = get_speaker_embedding(
                p, government, meeting_type, year, code, speakerID
            )
            add_weaviate(government, name, embedding)
            done.append(speakerID)


if __name__ == "__main__":
    print("Creating speaker collection")
    delete_collection("Speakers")
    create_speaker_collection()
    delete_collection("TranscriptsV2")
    print("Creating transcript collection")
    create_transcript_collection()

    data_path = "/app/data"
    for p in os.listdir(data_path):
        if not os.path.isdir(f"{data_path}/{p}") or p.startswith("."):
            continue
        print("Populating weaviate with", f"{data_path}/{p}")
        add_transcripts(f"{data_path}/{p}")


    # SPEAKERS INSERTS
    annotated_files_2023_hoekschewaard = [
        f"{data_path}/hoekschewaard/vergaderingen/2023/sheets/1068470.wav.rttm.xlsx",
        f"{data_path}/hoekschewaard/vergaderingen/2023/sheets/1068534.wav.rttm.xlsx",
        f"{data_path}/hoekschewaard/vergaderingen/2023/sheets/1068543.wav.rttm.xlsx",
        f"{data_path}/hoekschewaard/vergaderingen/2023/sheets/1109657.wav.rttm.xlsx",
    ]
    annotated_files_2024_hoekschewaard = [
        f"{data_path}/hoekschewaard/vergaderingen/2024/sheets/1178278.wav.rttm.xlsx",
        f"{data_path}/hoekschewaard/vergaderingen/2024/sheets/1178261.wav.rttm.xlsx",
        f"{data_path}/hoekschewaard/vergaderingen/2024/sheets/1192781.wav.rttm.xlsx",
    ]
    for path in annotated_files_2023_hoekschewaard:
        try:
            handle_file("hoekschewaard", "vergadering", "2023", path)
        except Exception as e:
            print("error in", path, e)
    for path in annotated_files_2024_hoekschewaard:
        try:
            handle_file("hoekschewaard", "vergadering", "2024", path)
        except Exception as e:
            print("error in", path, e)

    annotated_files_2023_ridderkerk = [
        f"{data_path}/ridderkerk/vergaderingen/2023/sheets/1068434.wav.rttm.xlsx",
        f"{data_path}/ridderkerk/vergaderingen/2023/sheets/1068445.wav.rttm.xlsx",
    ]
    annotated_files_2024_ridderkerk = [
        f"{data_path}/ridderkerk/vergaderingen/2024/sheets/1147151.wav.rttm.xlsx",
        f"{data_path}/ridderkerk/vergaderingen/2024/sheets/1147158.wav.rttm.xlsx",
        f"{data_path}/ridderkerk/vergaderingen/2024/sheets/1147176.wav.rttm.xlsx",
        f"{data_path}/ridderkerk/vergaderingen/2024/sheets/1147208.wav.rttm.xlsx",
    ]
    for path in annotated_files_2023_ridderkerk:
        try:
            handle_file("ridderkerk", "vergadering", "2023", path)
        except Exception as e:
            print("error in", path, e)
    for path in annotated_files_2024_ridderkerk:
        try:
            handle_file("ridderkerk", "vergadering", "2024", path)
        except Exception as e:
            print("error in", path, e)

    annotated_files_2023_barendrecht = [
        f"{data_path}/barendrecht/vergaderingen/2023/sheets/1094927.wav.rttm.xlsx",
        f"{data_path}/barendrecht/vergaderingen/2023/sheets/1108841.wav.rttm.xlsx",
        f"{data_path}/barendrecht/vergaderingen/2023/sheets/1115813.wav.rttm.xlsx",
    ]
    annotated_files_2024_barendrecht = [
        f"{data_path}/barendrecht/vergaderingen/2024/sheets/1195585.wav.rttm.xlsx",
        f"{data_path}/barendrecht/vergaderingen/2024/sheets/1203464.wav.rttm.xlsx",
        f"{data_path}/barendrecht/vergaderingen/2024/sheets/1203469.wav.rttm.xlsx",
        f"{data_path}/barendrecht/vergaderingen/2024/sheets/1223517.wav.rttm.xlsx",
    ]
    for path in annotated_files_2023_barendrecht:
        try:
            handle_file("barendrecht", "vergadering", "2023", path)
        except Exception as e:
            print("error in", path, e)
    for path in annotated_files_2024_barendrecht:
        try:
            handle_file("barendrecht", "vergadering", "2024", path)
        except Exception as e:
            print("error in", path, e)
