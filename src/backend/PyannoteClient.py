import os
import torch

from UserTypes import PyannoteReturnCodes

from dotenv import load_dotenv

from pyannote.audio import Pipeline
from pyannote.audio import Inference
from pyannote.audio import Model
from pyannote.core import Segment

load_dotenv()


class Pyannote:
    def __init__(self, device):
        self.diorize_pipeline = Pipeline.from_pretrained(
            "pyannote/speaker-diarization-3.1",
            use_auth_token=os.getenv("HF_PYANNOTE_ACCESS_TOKEN"),
        )
        self.diorize_pipeline.to(torch.device(device))

        # self.inference = Inference(
        #     Model.from_pretrained(
        #         "pyannote/embedding",
        #         os.getenv("HF_PYANNOTE_ACCESS_TOKEN"),
        #     ),
        #     window="whole",
        # )
        # self.inference.to(torch.device(device))

    def diorize(self, input_file, output_file):
        if not input_file.endswith(".wav"):
            return PyannoteReturnCodes.NO_WAV_FILE

        diarization = self.diorize_pipeline(input_file)

        if not os.path.exists(input_file):
            return PyannoteReturnCodes.INPUTFILE_DOES_NOT_EXIST
        if os.path.exists(output_file):
            return PyannoteReturnCodes.OUPUTFILE_ALREADY_EXISTS

        with open(output_file, "w") as rttm:
            diarization.write_rttm(rttm)

    def embed(self, input_file, output_file, from_time, to_time):
        excerpt = Segment(from_time, to_time)
        embedding = self.inference.crop(input_file, excerpt)
        print(embedding)  # tmp
