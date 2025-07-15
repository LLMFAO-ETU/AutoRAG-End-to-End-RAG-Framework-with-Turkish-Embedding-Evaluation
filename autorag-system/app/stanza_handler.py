import stanza
import os

def initialize_stanza_pipeline (lang="tr"):
    """
    Stanza modelini indirir (mevcut değilse).
    """
    default_dir = os.path.join(os.path.expanduser("~"), "stanza_resources")
    lang_dir = os.path.join(default_dir, lang)
    tokenizer_file = os.path.join(lang_dir, "tokenizer", f"{lang}_tokenizer.pt")

    if not os.path.exists(tokenizer_file):
        print(f"[INFO] Stanza Türkçe modeli indiriliyor: {default_dir}")
        stanza.download(lang)
    else:
        print(f"[INFO] Stanza Türkçe modeli zaten mevcut: {default_dir}")

    try:
        pipeline = stanza.Pipeline(lang=lang)
        _ = pipeline("Test cümlesi.")  # zorunlu preload
        return pipeline
    except Exception as e:
        print("[HATA] pipeline oluşturulamadı:", e)
        raise
