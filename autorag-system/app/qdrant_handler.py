from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from tqdm import tqdm
import time

def connect_qdrant():
    """
    Lokal Docker Qdrant container'ına bağlanır.
    """
    client = QdrantClient(
        url="http://localhost:6333",
        prefer_grpc=False,
        timeout=60.0
    )
    return client

def recreate_collection(qdrant_client, collection_name, vector_size):
    """
    Varsa dokunma, yoksa oluştur.
    """
    try:
        qdrant_client.get_collection(collection_name=collection_name)
        return
    except Exception:
        pass

    qdrant_client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
    )

def upload_points_to_qdrant(qdrant_client, collection_name, embeddings, metadata_list, batch_size=1024):
    """
    Embedding ve metadata verilerini Qdrant'a yükler.
    """
    points = [
        {
            "id": idx,
            "vector": embeddings[idx].tolist(),
            "payload": metadata_list[idx]
        }
        for idx in range(len(embeddings))
    ]

    uploaded_total = 0
    for i in tqdm(range(0, len(points), batch_size), desc="Qdrant'a yükleniyor"):
        batch = points[i:i + batch_size]
        try:
            qdrant_client.upsert(collection_name=collection_name, points=batch)
            uploaded_total += len(batch)
        except Exception as e:
            print(f"[!] Batch {i}-{i + batch_size} yüklenemedi: {e}")
            time.sleep(2)

    print(f"Toplam {uploaded_total} nokta Qdrant'a yüklendi.")

