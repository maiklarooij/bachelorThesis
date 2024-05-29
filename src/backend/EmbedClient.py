from sentence_transformers import SentenceTransformer
from gritlm import GritLM

from UserTypes import EmbedReturnCodes


class Embedder:
    def __init__(self):
        print("Init method not implemented!")
        return EmbedReturnCodes.NOT_IMPLEMENTED

    def embed(self, text):
        if not self.model:
            return EmbedReturnCodes.NO_MODEL

        return self.model.encode(text)


# https://huggingface.co/Salesforce/SFR-Embedding-Mistral
class SFRMistralEmbedder(Embedder):
    def __init__(self):
        self.model = SentenceTransformer("Salesforce/SFR-Embedding-Mistral")


# https://huggingface.co/GritLM/GritLM-7B
class GritEmbedder(Embedder):
    def __init__(self):
        self.model = GritLM("GritLM/GritLM-7B", torch_dtype="auto", mode="embedding")


# https://huggingface.co/sentence-transformers/all-mpnet-base-v2
class MpnetEmbedder(Embedder):
    def __init__(self):
        self.model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")
