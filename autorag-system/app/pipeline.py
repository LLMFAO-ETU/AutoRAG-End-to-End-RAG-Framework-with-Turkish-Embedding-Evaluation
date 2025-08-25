def autorag_process(zip_file_path: str, question: str, top_k_size: int, embedding_model, llm_model, collection_name: str):
    from app.embedding import get_embedder
    from app.document_parser import load_documents
    from app.chunker import batch_create_pre_segments, finalize_chunks_from_pre_segments
    from app.qdrant_handler import connect_qdrant, recreate_collection, upload_points_to_qdrant
    from app.generator import rag_answer
    from app.stanza_handler import initialize_stanza_pipeline
    import numpy as np
    from itertools import groupby
    from tqdm import tqdm

    # 1. Embedder ve NLP başlat
    embed_model = get_embedder(embedding_model)
    nlp_tr = initialize_stanza_pipeline("tr")

    # 2. Belgeleri yükle
    all_documents = load_documents(zip_file_path, use_unstructured_primarily=False)

    # 3. Pre-segment + embed
    all_pre_segments = batch_create_pre_segments(all_documents, nlp_tr)
    texts = [item['text'] for item in all_pre_segments]
    embeddings = embed_model.encode(texts, batch_size=128, show_progress_bar=True, convert_to_numpy=True)

    for i, item in enumerate(all_pre_segments):
        item['embedding'] = embeddings[i]

    # 4. Final chunk + metadata
    final_chunks_text, metadata = [], []
    for source, group in tqdm(groupby(all_pre_segments, key=lambda x: x['source']), total=len(all_documents)):
        group = list(group)
        group_texts = [x['text'] for x in group]
        group_embeds = np.array([x['embedding'] for x in group])
        final_chunks = finalize_chunks_from_pre_segments(group_texts, group_embeds)
        for i, chunk in enumerate(final_chunks):
            if chunk.strip():
                final_chunks_text.append(chunk)
                metadata.append({
                    "source": source,
                    "chunk_id_in_file": i,
                    "original_text": chunk
                })

    final_embeddings = embed_model.encode(final_chunks_text, batch_size=128, show_progress_bar=True, convert_to_numpy=True)

    # 5. Qdrant'a yükle
    client = connect_qdrant()
    recreate_collection(client, collection_name, final_embeddings.shape[1])
    upload_points_to_qdrant(client, collection_name, final_embeddings, metadata)

    # 6. Soruya cevap ver
    return rag_answer(question, top_k_size, llm_model, embedding_model, collection_name)
