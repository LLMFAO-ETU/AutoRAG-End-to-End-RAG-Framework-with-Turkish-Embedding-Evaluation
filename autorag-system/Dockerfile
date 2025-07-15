FROM python:3.10-slim

ENV LANG C.UTF-8

# Sistem paketleri
RUN apt-get update && apt-get install -y \
    git curl unzip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

COPY requirements.txt ./
COPY app ./app
COPY main.py ./

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

RUN python -c "import stanza; stanza.download('tr')"

ENTRYPOINT ["python", "main.py"]
