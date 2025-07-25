import os

# TensorFlow’u devre dışı bırak
os.environ["USE_TF"] = "0"
os.environ["TRANSFORMERS_NO_TF"] = "1"
os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'

# Embedding modeli
EMBED_MODEL_NAME = "sentence-transformers/distiluse-base-multilingual-cased-v1"
