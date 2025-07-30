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

## 📬 İletişim

Bu projeyle ilgili bir sorun yaşarsanız veya katkı sunmak isterseniz lütfen iletişime geçin.

© 2025 AutoRAG | Türkçe RAG sistemleri için açık kaynaklı çözüm 💬
