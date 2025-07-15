from app.embedding import get_embedder
from app.config import COLLECTION_NAME

def retrieve_top_k(query: str, qdrant_client, k: int = 5):
    """
    Verilen sorgu için Qdrant vektör veri tabanından en benzer k chunk'ı döndürür.
    """
    embed_model = get_embedder()
    q_emb = embed_model.encode([query], convert_to_numpy=True)[0]

    search_result = qdrant_client.search(
        collection_name=COLLECTION_NAME,
        query_vector=q_emb.tolist(),
        limit=k,
        with_payload=True
    )

    results = []
    for hit in search_result:
        payload = hit.payload
        score = hit.score
        src = payload.get("source", "<unknown_source>")
        chunk_id_file = payload.get("chunk_id_in_file", -1)
        text = payload.get("original_text", "<text_not_found_in_payload>")

        results.append({
            "source": src,
            "chunk_id_in_file": chunk_id_file,
            "score": score,
            "text": text
        })

    return results
