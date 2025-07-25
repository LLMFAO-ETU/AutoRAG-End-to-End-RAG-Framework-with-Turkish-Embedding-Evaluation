from sentence_transformers import SentenceTransformer
from app.config import EMBED_MODEL_NAME

def get_embedder(model_name):
    """
    SentenceTransformer modelini yükler ve döndürür.
    """
    try:
        model = SentenceTransformer(model_name)
        return model
    except Exception as e:
        print(f"Embedding modeli yüklenirken hata oluştu: {e}")
        return None
