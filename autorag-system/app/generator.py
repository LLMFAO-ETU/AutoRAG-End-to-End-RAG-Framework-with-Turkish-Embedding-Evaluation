import requests
import os
from app.retriever import retrieve_top_k
from app.qdrant_handler import connect_qdrant

def ollama_generate(prompt, model, max_tokens=1024, temperature=0.6):

    api_url = os.getenv("OLLAMA_API", "http://localhost:11434") + "/api/generate"

    
    print(f">>> Ollama API isteği başlatılıyor (Model: {model})...")
    
    try:
        response = requests.post(
            api_url,
            json={
                "model": model,
                "prompt": prompt,
                "stream": False, 
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens,
                    "top_p": 0.9
                }
            }
        )
        response.raise_for_status() # 4xx veya 5xx gibi HTTP hata kodlarında istisna fırlatır.
        
        json_data = response.json()
        return json_data.get("response", "[Ollama'dan boş yanıt döndü]").strip()

    except requests.exceptions.ConnectionError as e:
        print(f"HATA: Ollama sunucusuna bağlanılamadı. Ollama'nın çalıştığından emin olun.")
        print(f"Detay: {e}")
        return "[HATA: OLLAMA SUNUCUSUNA BAĞLANILAMADI]"
    except requests.exceptions.RequestException as e:
        print(f"Ollama API isteği sırasında bir hata oluştu: {e}")
        return f"[HATA: API İSTEĞİ BAŞARISIZ: {e.response.text if e.response else 'Yanıt yok'}]"
    except Exception as e:
        print(f"Beklenmedik bir istisna oluştu: {e}")
        return "[HATA: BEKLENMEDİK İSTİSNA]"


def rag_answer(query: str, k: int, model: str, embed_model: str, collection_name: str):
    
    print("\n>> Qdrant bağlantısı kuruluyor...")
    qdrant_client = connect_qdrant()

    print(">> Top-K retrieve ediliyor...")
    results = retrieve_top_k(query, qdrant_client, k, embed_model, collection_name)

    if not results:
        print("Qdrant sonuç döndürmedi.")
        return "[Bilgi bulunamadı]"

    print(">> Prompt oluşturuluyor...")
    sources_text = "\n\n".join(
        f"[{i+1}] Skor: {r['score']:.4f}\n{r['text']}"
        for i, r in enumerate(results)
    )

    prompt = (
        "Sen bir Türkçe NLP uzmanısın. Lütfen cevabını sadece Türkçe olarak ver."
        f"Soru: {query}\n\n"
        "Yukarıdaki soruyu, aşağıda verilen kaynakları kullanarak yanıtla. Sadece kaynaklarda geçen bilgileri kullan.\n\n"
        f"Kaynaklar:\n{sources_text}\n\n"
        "Yanıt:" 
    )

    answer = ollama_generate(prompt,model)

    print(">> Yanıt alındı.")
    return answer
    