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
