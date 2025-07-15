
# 🧠 AutoRAG — Belge Tabanlı Cevaplama Sistemi (Docker Sürümü)

AutoRAG, `.pdf`, `.docx` ve `.txt` dosyalarını işleyerek anlamlı parçalara bölen, embedding’lerini çıkaran, Qdrant vektör veritabanına kaydeden ve Ollama LLM API ile Türkçe sorulara doğru ve kaynaklı cevaplar veren modern bir Retrieval-Augmented Generation (RAG) sistemidir.

---

## ⚙️ Kurulum ve Çalıştırma Adımları

### 🧩 1. Bu klasörü bilgisayarınıza indirin

GitHub’dan veya doğrudan `.zip` olarak edindiğiniz dosyaları bir klasöre çıkarın. Örnek yapı şöyle olmalıdır:

```
autorag-system/
├── docker-compose.yml
├── Dockerfile
├── main.py
├── requirements.txt
├── app/
│   ├── *.py
└── data/
    └── belgeler.zip   ← belgelerinizi buraya koyacaksınız
```

### 🐳 2. Docker image’ini oluşturun

Terminali bu klasörde açın ve aşağıdaki komutla Docker image’ini oluşturun:

```bash
docker-compose build
```

> Bu işlem ilk seferde birkaç dakika sürebilir. Gerekli Python kütüphaneleri indirilecektir.

### ⚡ 3. Sistemi çalıştırın

Belgelerinizi `data/` klasörüne `.zip` formatında koyduktan sonra şu komutu çalıştırın:

```bash
docker-compose run --rm autorag --file /data/belgeler.zip --query "Belgelerinizle ilgili soruyu buraya yazın"
```

✅ Örnek:

```bash
docker-compose run --rm autorag --file /data/ataturk.zip --query "Atatürk'ün ekonomi politikaları nasıldı?"
```


### 🧼 4. Kullanımı bitirdikten sonra sistem servislerini durdurun

```bash
docker-compose down
```

## 💡 Yardımcı Notlar

- Docker Desktop kurulu değilse: [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)
- `docker-compose` komutu tanınmıyorsa, `docker compose` (boşluklu) şeklinde deneyebilirsiniz.

## 🧩 Tam Komutlar Zinciri (Kopyala-yapıştır için)

```bash
# 1. Projeyi bir klasöre çıkarın
cd autorag-system

# 2. Docker image oluştur
docker-compose build

# 3. Belgeleri data/ içine koy
mv ~/Downloads/belgeler.zip ./data/

# 4. Sistemi çalıştır
docker-compose run --rm autorag --file /data/belgeler.zip --query "Belgelerin içeriğine dair sorunuz"

# 5. İşiniz bittiğinde durdur
docker-compose down
```

---

## 🔍 Nasıl Çalışır?

1. `.zip` dosyası açılır, `.pdf`, `.docx`, `.txt` dosyaları ayrıştırılır.
2. Her doküman, `Stanza` ile cümlelere bölünerek anlamlı segmentlere ayrılır.
3. Bu segmentler `sentence-transformers` ile embedding’e dönüştürülür.
4. `Qdrant` vektör veritabanına kayıt edilir.
5. Soru için embedding çıkarılır, Qdrant’tan en yakın parçalar alınır.
6. Bu parçalar prompt’a eklenip `Ollama` üzerinden `gemma:2b` ile cevap alınır.

## 🛠️ Teknik Detaylar

| Bileşen       | Teknoloji                         |
|---------------|-----------------------------------|
| Dil modeli    | `gemma:2b` (via Ollama)          |
| Embedding     | `distiluse-base-multilingual-cased-v1` |
| Parser        | `unstructured`, `stanza`, `pypdf`, `python-docx` |
| Vector DB     | Qdrant                           |
| Docker Image  | AutoRAG (yerel build)            |

## 🧪 Örnek Sorgular

```bash
docker-compose run --rm autorag --file /data/raporlar.zip --query "Dijital dönüşüm nedir?"
```

```bash
docker-compose run --rm autorag --file /data/tarih.zip --query "Kapitülasyonların kaldırılması ne zaman gerçekleşti?"
```

## 📬 İletişim

Bu projeyle ilgili bir sorun yaşarsanız veya katkı sunmak isterseniz lütfen iletişime geçin.

© 2025 AutoRAG | Türkçe RAG sistemleri için açık kaynaklı çözüm 💬
