from sentence_transformers import SentenceTransformer

def get_embedder(model_name):
    """
    SentenceTransformer modelini uygun parametrelerle yükler ve döndürür.
    """
    try:
        if "Trendyol/TY-ecomm-embed" in model_name:
            return SentenceTransformer(model_name, trust_remote_code=True)
        else:
            return SentenceTransformer(model_name)
    except Exception as e:
        print(f"Embedding modeli yüklenirken hata oluştu: {e}")
        return None