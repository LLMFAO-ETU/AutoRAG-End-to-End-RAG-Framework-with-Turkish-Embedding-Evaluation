# 🧠 AutoRAG — Belge Tabanlı Cevaplama Sistemi (Docker + GUI )

**AutoRAG**, `.pdf`, `.docx`, `.txt`, `.md` ve `.zip` gibi dosyaları işleyerek anlamlı parçalara bölen, embedding’lerini çıkaran, Qdrant vektör veritabanına kaydeden ve Ollama LLM API üzerinden Türkçe sorulara doğru ve kaynaklı cevaplar veren modern bir **Retrieval-Augmented Generation (RAG)** sistemidir.

Yeni sürümle birlikte artık kullanıcı dostu **web arayüzü (GUI)** üzerinden tüm işlemleri gerçekleştirebilirsiniz!

---

## 🔍 Nasıl Çalışır?

1. Yüklenen dosya (tekil veya `.zip`) açılır, `.pdf`, `.docx`, `.txt`, `.md` belgeler ayrıştırılır.
2. Cümlelere ayrılma işlemi `Stanza` ile yapılır.
3. Segmentler, seçilen **embedding modeli** ile vektörleştirilir.
4. Bu vektörler **Qdrant** veritabanına kaydedilir.
5. Kullanıcının sorusu embedlenir, Qdrant’tan en yakın parçalar getirilir.
6. Bu parçalar prompt’a gömülerek seçilen **LLM modeli** ile cevap üretilir.

---

## 🛠️ Teknik Detaylar

| Bileşen                  | Teknoloji / Açıklama |
|--------------------------|----------------------|
| **Dil Modelleri (LLM)**  | `mistral:instruct`, `gemma:2b`, `Phi-2` *(Ollama ile local çalışır)* |
| **Embedding Modelleri**  | `sentence-transformers/distiluse-base-multilingual-cased-v1`<br>`sentence-transformers/distiluse-base-multilingual-cased-v2`<br>`Trendyol/TY-ecomm-embed-multilingual-base-v1.2.0` |
| **Parserlar**            | `unstructured`, `stanza`, `python-docx`, `pypdf` |
| **Vektör Veritabanı**    | `Qdrant` |
| **Arayüz**               | `Gradio` tabanlı web arayüz (localhost:7860) |
| **Docker Ortamı**        | `docker-compose` ile izole ve hızlı kurulum |

**Not:**  
Kullanılan dil modelleri (LLM), Türkçe dilinde yeterli performans sergileyen, düşük parametreli ve localde çalıştırılabilir modellerden seçilmiştir. Büyük ve daha başarılı modeller yerine bu seçenekler tercih edilmiştir çünkü hedef, sistemin donanım dostu, hızlı ve erişilebilir olmasıdır.

---

## ⚙️ Kurulum ve Çalıştırma Adımları

### Proje Yapısı

GitHub’dan veya `.zip` olarak projeyi indirip çıkartın. Klasör yapısı şu şekilde olmalıdır:

```
autorag-system/
├── docker-compose.yml
├── Dockerfile
├── main.py
├── requirements.txt
├── app/
│   ├── *.py
└── data/
    └── belgeler.zip   ← belgelerinizi buraya koyabilirsiniz (isteğe bağlı)
```

**Not:**  
`data/` klasörüne belge koymak, terminalde `--file` argümanını kullanacak CLI kullanıcıları içindir. GUI arayüzü kullananlar belgeyi doğrudan arayüzden yükleyebilir, klasöre koymak zorunda değildir.

---

## 🧾 Tam Kurulum ve Çalıştırma Komutları (GUI Modu)

```bash
# 1. Projeyi bir klasöre çıkarın
cd autorag-system

# 2. Docker image oluştur > Bu işlem ilk seferde uzun sürebilir. Gerekli Python kütüphaneleri indirilecektir.
docker-compose build

# 3. (Opsiyonel) Belgeleri data/ klasörüne kopyalayın
mv ~/Downloads/belgeler.zip ./data/

# 4. Sistemi başlatın
docker-compose run --rm autorag

# Tarayıcınızda http://localhost:7860 adresini manuel olarak açın.

# 5. İşiniz bittiğinde sistemi kapatın
docker-compose down
```

---

## 🖥️ Alternatif: Terminal (CLI) Modu

AutoRAG, GUI dışında terminal üzerinden çalıştırılabilir bir komut satırı arayüzü de sunar. Bu mod, daha hızlı sorgular yapmak veya GUI arayüzü olmadan sistemle etkileşime geçmek isteyen kullanıcılar için uygundur.

### 🔹 Zorunlu argümanlar:
- `--file` : `.zip` dosyasının yolu
- `--query` : sorulacak metin

### 🔸 İsteğe bağlı argümanlar:
- `--embed` : embedding modeli adı *(varsayılan: `sentence-transformers/Trendyol/TY-ecomm-embed-multilingual-base-v1.2.0`)*
- `--llm` : LLM modeli adı *(varsayılan: `mistral:instruct`)*
- `--topk` : kaç chunk alınacağı *(varsayılan: `8`)*

### ✅ Önerilen kullanım:

```bash
docker-compose run --rm autorag   --file /data/ataturk.zip   --query "Atatürk'ün ekonomi politikaları nasıldı?"
```

### 🔧 Gelişmiş kullanım:

```bash
docker-compose run --rm autorag   --file /data/ataturk.zip   --query "Atatürk'ün ekonomi politikaları nasıldı?"   --embed distiluse-base-multilingual-cased-v1   --llm gemma:2b   --topk 5
```

---
## 📊 Retrieval Performance Metrics
### Longest Wikipedia Segment Selection
| Metric  | Embedding Model                                  | Top-k = 3 | Top-k = 5 | Top-k = 8 | Top-k = 10 |
| ------- | ------------------------------------------------ | --------- | --------- | --------- | ---------- |
| Recall  | distiluse-base-multilingual-cased-v1             | 0.3111    | 0.3555    | 0.4222    | 0.4666     |
| Recall  | distiluse-base-multilingual-cased-v2             | 0.2889    | 0.3333    | 0.4222    | 0.4444     |
| Recall  | Trendyol/TY-ecomm-embed-multilingual-base-v1.2.0 | 0.3667    | 0.4333    | 0.5000    | 0.5333     |
| EIR     | distiluse-base-multilingual-cased-v1             | 0.0098    | 0.0064    | 0.0061    | 0.0045     |
| EIR     | distiluse-base-multilingual-cased-v2             | 0.0085    | 0.0067    | 0.0051    | 0.0030     |
| EIR     | Trendyol/TY-ecomm-embed-multilingual-base-v1.2.0 | 0.0114    | 0.0078    | 0.0058    | 0.0049     |
| nDCG\@k | distiluse-base-multilingual-cased-v1             | 0.2356    | 0.2452    | 0.2679    | 0.2825     |
| nDCG\@k | distiluse-base-multilingual-cased-v2             | 0.1972    | 0.2068    | 0.2374    | 0.2431     |
| nDCG\@k | Trendyol/TY-ecomm-embed-multilingual-base-v1.2.0 | 0.3265    | 0.3640    | 0.3827    | 0.3827     |

### Random Wikipedia Segment Selection
| Metric  | Embedding Model                                  | Top-k = 3 | Top-k = 5 | Top-k = 8 | Top-k = 10 |
| ------- | ------------------------------------------------ | --------- | --------- | --------- | ---------- |
| Recall  | distiluse-base-multilingual-cased-v1             | 0.5111    | 0.5556    | 0.6000    | 0.6222     |
| Recall  | distiluse-base-multilingual-cased-v2             | 0.4222    | 0.4667    | 0.4667    | 0.4889     |
| Recall  | Trendyol/TY-ecomm-embed-multilingual-base-v1.2.0 | 0.6333    | 0.7333    | 0.7333    | 0.7667     |
| EIR     | distiluse-base-multilingual-cased-v1             | 0.0464    | 0.0195    | 0.0129    | 0.0107     |
| EIR     | distiluse-base-multilingual-cased-v2             | 0.0275    | 0.0183    | 0.0113    | 0.0059     |
| EIR     | Trendyol/TY-ecomm-embed-multilingual-base-v1.2.0 | 0.0368    | 0.0235    | 0.0136    | 0.0090     |
| nDCG\@k | distiluse-base-multilingual-cased-v1             | 0.4399    | 0.4543    | 0.4693    | 0.4760     |
| nDCG\@k | distiluse-base-multilingual-cased-v2             | 0.3524    | 0.3715    | 0.3764    | 0.3826     |
| nDCG\@k | Trendyol/TY-ecomm-embed-multilingual-base-v1.2.0 | 0.5524    | 0.5913    | 0.5978    | 0.6161     |


### Shortest Wikipedia Segment Selection
| Metric  | Embedding Model                                  | Top-k = 3 | Top-k = 5 | Top-k = 8 | Top-k = 10 |
| ------- | ------------------------------------------------ | --------- | --------- | --------- | ---------- |
| Recall  | distiluse-base-multilingual-cased-v1             | 0.9286    | 0.9286    | 0.9286    | 0.9286     |
| Recall  | distiluse-base-multilingual-cased-v2             | 0.8571    | 0.8571    | 0.8571    | 0.9286     |
| Recall  | Trendyol/TY-ecomm-embed-multilingual-base-v1.2.0 | 1.0000    | 1.0000    | 1.0000    | 1.0000     |
| EIR     | distiluse-base-multilingual-cased-v1             | 0.1652    | 0.0902    | 0.0502    | 0.0388     |
| EIR     | distiluse-base-multilingual-cased-v2             | 0.1802    | 0.0884    | 0.0400    | 0.0314     |
| EIR     | Trendyol/TY-ecomm-embed-multilingual-base-v1.2.0 | 0.1244    | 0.0681    | 0.0337    | 0.0230     |
| nDCG\@k | distiluse-base-multilingual-cased-v1             | 0.8571    | 0.8571    | 0.8571    | 0.8571     |
| nDCG\@k | distiluse-base-multilingual-cased-v2             | 0.7687    | 0.7687    | 0.7687    | 0.7902     |
| nDCG\@k | Trendyol/TY-ecomm-embed-multilingual-base-v1.2.0 | 1.0000    | 1.0000    | 1.0000    | 1.0000     |

---

## 📬 İletişim

Bu projeyle ilgili bir sorun yaşarsanız veya katkı sunmak isterseniz lütfen iletişime geçin.

© 2025 AutoRAG | Türkçe RAG sistemleri için açık kaynaklı çözüm 💬
