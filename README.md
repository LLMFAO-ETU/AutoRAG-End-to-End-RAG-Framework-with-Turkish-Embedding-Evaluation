# 🧠 AutoRAG — Belge Tabanlı Cevaplama Sistemi (Docker + GUI Sürümü)

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

### 🧩 1. Bu klasörü bilgisayarınıza indirin

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

### 🐳 2. Docker image’ini oluşturun

Terminali bu klasörde açın ve aşağıdaki komutu çalıştırarak Docker image’ini oluşturun:

```bash
docker-compose build
```

> Bu işlem ilk seferde uzun sürebilir. Gerekli Python kütüphaneleri indirilecektir.

---

## 🚀 Sistemi Başlatma (GUI Modu)

Artık tüm işlemler tarayıcı tabanlı grafiksel arayüz (GUI) üzerinden yapılabilmektedir.

### ✅ Kullanıcıya sağlanan seçenekler:

- 📄 Belge yükleme (.pdf, .docx, .txt, .md, .zip)
- 🔍 Soru sorma
- 💡 Embedding modeli seçimi
- 🧠 LLM modeli seçimi
- 🔢 Top-K chunk sayısı ayarı

### Başlatmak için:

```bash
docker-compose run --rm autorag
```

Ardından tarayıcınızda şu adresi açın:

```
http://localhost:7860
```

---

## 🧾 Tam Komutlar Zinciri (Kopyala-Yapıştır için)

```bash
# 1. Projeyi bir klasöre çıkarın
cd autorag-system

# 2. Docker image oluştur
docker-compose build

# 3. (Opsiyonel) Belgeleri data/ klasörüne kopyalayın
mv ~/Downloads/belgeler.zip ./data/

# 4. Sistemi başlatın (GUI arayüzü için tarayıcınızda http://localhost:7860 adresini açın.)
docker-compose run --rm autorag

# 5. İşiniz bittiğinde sistemi kapatın
docker-compose down
```

---

## 🧼 Kullanımı Bitirdikten Sonra

```bash
docker-compose down
```

---


## 📬 İletişim

Bu projeyle ilgili bir sorun yaşarsanız veya katkı sunmak isterseniz lütfen iletişime geçin.

© 2025 AutoRAG | Türkçe RAG sistemleri için açık kaynaklı çözüm 💬
