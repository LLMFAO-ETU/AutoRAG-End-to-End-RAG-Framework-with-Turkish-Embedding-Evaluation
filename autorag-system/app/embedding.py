from sentence_transformers import SentenceTransformer
from app.config import EMBED_MODEL_NAME

def get_embedder():
    """
    SentenceTransformer modelini yükler ve döndürür.
    """
    return SentenceTransformer(EMBED_MODEL_NAME)
