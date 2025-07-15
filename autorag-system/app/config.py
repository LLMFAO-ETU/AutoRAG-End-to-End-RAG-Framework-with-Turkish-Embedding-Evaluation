import os

# TensorFlow’u devre dışı bırak
os.environ["USE_TF"] = "0"
os.environ["TRANSFORMERS_NO_TF"] = "1"
os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'

# Qdrant ayarları
#CLOUD_URL = "https://d8f9c106-88a7-4933-bb28-d6b7b23bdc02.us-east4-0.gcp.cloud.qdrant.io"
#API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.uQ8vYNls4ViEcO1TAApHP4CDcpquhV6P_ey49x75IB4"
COLLECTION_NAME = "llmfao_collection"

# Embedding modeli
EMBED_MODEL_NAME = "sentence-transformers/distiluse-base-multilingual-cased-v1"
