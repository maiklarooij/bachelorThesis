from fastapi import HTTPException

from UserTypes import WhisperReturnCodes

def verify_whisper_return_code(code):
    if code == WhisperReturnCodes.OK:
        return
    elif code == WhisperReturnCodes.TRANSCRIPTION_ALREADY_EXISTS:
        raise HTTPException(status_code=500, detail="Error in transcribing: Transcription already exists")
    elif code == WhisperReturnCodes.TRANSCRIPTION_DOES_NOT_EXIST:
        raise HTTPException(status_code=500, detail="Error in loading transcription: Transcription does not exist")
    elif code == WhisperReturnCodes.NO_TRANSCRIPTION:
        raise HTTPException(status_code=500, detail="Error in saving transcription: No transcription provided")
    elif code == WhisperReturnCodes.INVALID_MODEL:
        raise HTTPException(status_code=500, detail="Whisper client has invalid model")
    else:
        raise HTTPException(status_code=500, detail="Unknown whisper return code")
