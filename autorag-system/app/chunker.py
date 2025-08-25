from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm

def batch_create_pre_segments(
    all_documents: dict, 
    stanza_nlp_model,
    pre_segment_max_chars: int = 1000,
    pre_segment_max_sentences: int = 8
):
   
    print("\n[INFO] Tüm belgeler toplu olarak işleniyor.")
    print("[INFO] Bu işlem belgelerin toplam boyutuna göre birkaç dakika sürebilir. Lütfen bekleyin...")
    # Belgelerin yollarını ve içeriklerini ayrı listelere al
    doc_paths = list(all_documents.keys())
    doc_texts = list(all_documents.values())

    # 1. Stanza'yı tüm metinler üzerinde BATCH modunda çalıştır.
    processed_docs = stanza_nlp_model.bulk_process(doc_texts)
    
    # 2. İşlenmiş belgelerden ön-segmentleri çıkar.
    all_pre_segments_with_source = []
    
    # tqdm'i buraya taşıdık, böylece ilerleme daha anlamlı olur.
    for i in tqdm(range(len(doc_paths)), desc="Ön-segmentler çıkarılıyor"):
        path = doc_paths[i]
        doc = processed_docs[i]
        
        sentences = [" ".join([word.text for word in sentence.words]) for sentence in doc.sentences]

        if not sentences:
            continue

        # Ön-segment oluşturma mantığı
        current_pre_segment_sentences = []
        current_pre_segment_chars = 0
        for sentence in sentences:
            if (current_pre_segment_chars + len(sentence) > pre_segment_max_chars and current_pre_segment_sentences) or \
               (len(current_pre_segment_sentences) >= pre_segment_max_sentences):
                segment_text = " ".join(current_pre_segment_sentences)
                all_pre_segments_with_source.append({'source': path, 'text': segment_text})
                current_pre_segment_sentences = []
                current_pre_segment_chars = 0

            current_pre_segment_sentences.append(sentence)
            current_pre_segment_chars += len(sentence)
        
        if current_pre_segment_sentences:
            segment_text = " ".join(current_pre_segment_sentences)
            all_pre_segments_with_source.append({'source': path, 'text': segment_text})
            
    return all_pre_segments_with_source

# Hazır ön-segmentler ve embedding'lerden son chunkları oluşturur.
def finalize_chunks_from_pre_segments(
    pre_segments,
    pre_segment_embeddings,
    similarity_threshold: float = 0.40,
    final_chunk_min_pre_segments: int = 1,
    final_chunk_max_pre_segments: int = 6, # final chunk'ın yaklaşık 1020 token aralığı civarında olmasını sağlar.
):
    if not pre_segments:
        return []
    if len(pre_segments) == 1:
        return pre_segments

    final_chunks = []
    current_chunk = [pre_segments[0]]

    for i in range(1, len(pre_segments)):
        sim = cosine_similarity([pre_segment_embeddings[i]], [pre_segment_embeddings[i - 1]])[0][0]
        split = False

        if sim < similarity_threshold:
            split = True
        if len(current_chunk) >= final_chunk_max_pre_segments:
            split = True

        if split and len(current_chunk) >= final_chunk_min_pre_segments:
            final_chunks.append(" ".join(current_chunk))
            current_chunk = [pre_segments[i]]
        else:
            current_chunk.append(pre_segments[i])

    if current_chunk and len(current_chunk) >= final_chunk_min_pre_segments:
        final_chunks.append(" ".join(current_chunk))

    return [chunk for chunk in final_chunks if chunk.strip()]