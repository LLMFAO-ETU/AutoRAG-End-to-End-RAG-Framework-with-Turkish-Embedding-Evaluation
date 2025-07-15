import logging
logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')
import argparse
from app.config import *
from app.embedding import get_embedder
from app.document_parser import load_documents
from app.chunker import batch_create_pre_segments, finalize_chunks_from_pre_segments
from app.qdrant_handler import (
    connect_qdrant,
    recreate_collection,
    upload_points_to_qdrant
)
from app.generator import rag_answer
from app.stanza_handler import initialize_stanza_pipeline 
from tqdm import tqdm
from itertools import groupby
import numpy as np

if __name__ == "__main__":
    # --- 1. Argümanları Tanımlama ve Okuma ---
    parser = argparse.ArgumentParser(
        description="Belgeleri işleyip Qdrant'a yükleyen ve bir soruya cevap veren RAG sistemi."
    )
    parser.add_argument(
        "--file", 
        required=True, 
        help="İşlenecek .zip dosyasının konteyner içindeki yolu."
    )
    parser.add_argument(
        "--query", 
        required=True, 
        help="Sisteme sorulacak soru."
    )
    args = parser.parse_args()

    # --- 2. Modelleri Başlatma ---
    embed_model = get_embedder()

    print("[AŞAMA 1] Stanza modeli başlatılıyor...")
    try:
        nlp_tr = initialize_stanza_pipeline("tr")
        print("Stanza hazır.")
    except Exception as e:
        print(f"[HATA] Stanza yüklenirken hata: {e}")
        exit(1)

    # --- 3. Belgeleri Yükleme ve İşleme ---
    print(f"[AŞAMA 2] Belgeler yükleniyor: {args.file}")
    all_documents = load_documents(args.file, use_unstructured_primarily=True)
    
    print("[AŞAMA 3] Anlamsal Chunking süreci başlıyor...")
    
    # Adım 3.1: Ön-segmentleri oluştur
    all_pre_segments_with_source = batch_create_pre_segments(
        all_documents=all_documents,
        stanza_nlp_model=nlp_tr
    )

    if not all_pre_segments_with_source:
        print("Hiç ön-segment oluşturulamadı. İşlem durduruluyor.")
        exit(1)

    print(f"\n[AŞAMA 3.2] {len(all_pre_segments_with_source)} adet ön-segment için embedding'ler hesaplanıyor...")
    all_pre_segment_texts = [item['text'] for item in all_pre_segments_with_source]
    all_pre_segment_embeddings = embed_model.encode(
        all_pre_segment_texts, 
        show_progress_bar=True,
        convert_to_numpy=True
    )
    for i, item in enumerate(all_pre_segments_with_source):
        item['embedding'] = all_pre_segment_embeddings[i]

    print("\n[AŞAMA 3.3] Anlamsal chunk'lar birleştiriliyor...")
    final_chunks_text = []
    metadata_for_qdrant = []
    
    for source_path, group in tqdm(groupby(all_pre_segments_with_source, key=lambda x: x['source']), desc="Chunk'lar sonlandırılıyor", total=len(all_documents)):
        group_items = list(group)
        group_pre_segments = [item['text'] for item in group_items]
        group_embeddings = np.array([item['embedding'] for item in group_items])
        
        final_chunks_for_doc = finalize_chunks_from_pre_segments(
            group_pre_segments,
            group_embeddings
        )
        
        for i, chunk_text in enumerate(final_chunks_for_doc):
            if chunk_text.strip():
                final_chunks_text.append(chunk_text)
                metadata_for_qdrant.append({
                    "source": source_path,
                    "chunk_id_in_file": i,
                    "original_text": chunk_text
                })
    
    if not final_chunks_text:
        print("Hiç son chunk oluşturulamadı. İşlem durduruluyor.")
        exit(1)
        
    print(f"\nToplam {len(final_chunks_text)} adet son chunk oluşturuldu.")

    print("Qdrant'a yüklenecek nihai embedding'ler oluşturuluyor...")
    final_embeddings_for_qdrant = embed_model.encode(final_chunks_text, show_progress_bar=True, convert_to_numpy=True)

    # --- 4. Qdrant'a Yükleme ---
    print("\n[AŞAMA 4] Qdrant veritabanı hazırlanıyor...")
    qdrant_client = connect_qdrant()
    recreate_collection(qdrant_client, COLLECTION_NAME, final_embeddings_for_qdrant.shape[1])
    upload_points_to_qdrant(qdrant_client, COLLECTION_NAME, final_embeddings_for_qdrant, metadata_for_qdrant)

    # --- 5. Sorguyu Yanıtlama ---
    print("\n[AŞAMA 5] Sağlanan soru yanıtlanıyor...")
    print("="*50)
    print(f"SORGU: {args.query}")
    final_answer = rag_answer(args.query) # rag_answer'ın içinde ollama kullandığını varsayıyoruz
    print("\nYANIT:\n", final_answer)
    print("="*50)