from typing import List, Any, Dict, Optional
from pydantic import BaseModel

class WhisperReturnCodes:
    OK = 0
    OTHER_ERROR = 1
    NOT_IMPLEMENTED = 2
    INVALID_MODEL = 3
    TRANSCRIPTION_ALREADY_EXISTS = 4
    TRANSCRIPTION_DOES_NOT_EXIST = 5
    NO_TRANSCRIPTION = 6
    INPUTFILE_DOES_NOT_EXIST = 7


class EmbedReturnCodes:
    OK = 0
    OTHER_ERROR = 1
    NOT_IMPLEMENTED = 2
    NO_MODEL = 3


class PyannoteReturnCodes:
    OK = 0
    INPUTFILE_DOES_NOT_EXIST = 1
    OUPUTFILE_ALREADY_EXISTS = 2
    NO_WAV_FILE = 3


class TranscribeBody(BaseModel):
    input_path: str
    output_path: str


class DiorizeBody(BaseModel):
    input_path: str
    output_path: str


class SpeechEmbedBody(BaseModel):
    input_path: str
    output_path: str
    from_time: float
    to_time: float


class Property(BaseModel):
    name: str
    data_type: str

class WeaviateCreateCollectionBody(BaseModel):
    name: str
    vector_index_hnsw: bool
    distance_config: str
    properties: List[Property]
    # TODO: BM25 settings

class WeaviateInsertBody(BaseModel):
    collection: str
    objects: List[Dict[str, Any]]

class WeaviateGetCollectionBody(BaseModel):
    collection: str

class WeaviateSearchHybridBody(BaseModel):
    collection: str
    query: str
    vector: List[float]
    limit: int
    alpha: float
    target_vec: str
    government: List[str]
    meetingType: List[str]
    year: List[str]
    speaker: List[str]
    video: List[str]
    query_properties: Optional[List[str]] = None

class WeaviateSearchBM25Body(BaseModel):
    collection: str
    query: str
    limit: int
    target_vec: str
    government: List[str]
    meetingType: List[str]
    year: List[str]
    speaker: List[str]
    video: List[str]
    query_properties: Optional[List[str]] = None

class WeaviateSearchVectorBody(BaseModel):
    collection: str
    vector: List[float]
    limit: int
    target_vec: str
    government: List[str]
    meetingType: List[str]
    year: List[str]
    speaker: List[str]
    video: List[str]

class WeaviateGetContext(BaseModel):
    collection: str
    government: str
    meetingType: str
    year: str
    speaker: str
    video: str
    speechNum: int


class WeaviateDeleteCollectionBody(BaseModel):
    collection: str

class EmbedBody(BaseModel):
    text: List[str]

class AgendaBody(BaseModel):
    full_text: str
    agenda_points: List[Dict[str, str]]

class ChatBody(BaseModel):
    history: List[Dict[Any, Any]]

class TranslateBody(BaseModel):
    text: str
