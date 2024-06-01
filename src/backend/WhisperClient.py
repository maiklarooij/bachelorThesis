import os
import platform
import json
import huggingface_hub

from UserTypes import WhisperReturnCodes

import whisper

if platform.system() == "Darwin":
    import whisperMLX

# Base transcriber class.
class Transcriber:
    def transcribe(self, input_file, output_file):
        print("Transcribe method not implemented!")
        return  WhisperReturnCodes.NOT_IMPLEMENTED

    def load_transcription(self, path):
        if not os.path.isfile(path):
            return WhisperReturnCodes.TRANSCRIPTION_DOES_NOT_EXIST

        with open(path, "r") as f:
            transcription = json.load(f)

        return transcription

    def regular_save_transcription(self, transcription, path):
        if not transcription:
            return WhisperReturnCodes.NO_TRANSCRIPTION

        with open(path, "w+") as f:
            json.dump(transcription, f)

        return WhisperReturnCodes.OK


# MLX transcriber class. To be used on amd Apple devices for faster inference.
class MLX_Transcriber(Transcriber):
    def __init__(self, model):
        self.model = model

    def transcribe(self, input_file, output_file):
        if not os.path.exists(input_file):
            return WhisperReturnCodes.INPUTFILE_DOES_NOT_EXIST
        # If transcription already exists, do not redo it.
        if os.path.exists(output_file):
            return WhisperReturnCodes.TRANSCRIPTION_ALREADY_EXISTS

        print(f"Transcribing {input_file}.")
        try:
            transcription = whisperMLX.transcribe(
                input_file,
                path_or_hf_repo=self.model,
                language= "nl",
            )
        except huggingface_hub.utils.RepositoryNotFoundError as e:
            return WhisperReturnCodes.INVALID_MODEL

        return self.regular_save_transcription(transcription, output_file)


# Pytorch transcriber class. To be used on NVIDIA GPUs or a regular cpu for
# faster inference.
class Torch_Transcriber(Transcriber):
    def __init__(self):
        self.model = whisper.load_model("medium")  # Model automatically tries cuda.

    def transcribe(self, input_file, output_file):
        # If transcription already exists, do not redo it.
        if os.path.exists(output_file):
            return WhisperReturnCodes.TRANSCRIPTION_ALREADY_EXISTS

        print(f"Transcribing {input_file}.")
        try:
            transcription = self.model.transcribe(
                input_file, decode_options={"language": "nl"}
            )
        except Exception as e:
            print("Error transcribing!", e)
            return WhisperReturnCodes.OTHER_ERROR

        return self.regular_save_transcription(transcription, output_file)
