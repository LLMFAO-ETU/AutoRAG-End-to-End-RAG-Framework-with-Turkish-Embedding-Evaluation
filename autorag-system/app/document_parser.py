import os
import glob
import logging
import zipfile
import docx
from pypdf import PdfReader
from unstructured.partition.auto import partition

# Logging ayarları
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def parse_with_unstructured(path):
    try:
        elements = partition(filename=path)
        return "\n".join(str(el.text) for el in elements if hasattr(el, 'text') and el.text)
    except Exception as e:
        logging.error(f"Unstructured ile '{path}' ayrıştırılırken hata: {e}")
        if path.lower().endswith(".pdf"):
            return parse_pdf_pypdf(path)
        elif path.lower().endswith(".docx"):
            return parse_docx_python_docx(path)
        elif path.lower().endswith(".txt"):
            return parse_txt_native(path)
        return None


def parse_pdf_pypdf(path):
    try:
        reader = PdfReader(path)
        text_parts = [page.extract_text() for page in reader.pages if page.extract_text()]
        return "\n".join(text_parts) if text_parts else None
    except Exception as e:
        logging.error(f"pypdf ile PDF '{path}' ayrıştırılırken hata: {e}")
        return None


def parse_docx_python_docx(path):
    try:
        doc = docx.Document(path)
        return "\n".join(p.text for p in doc.paragraphs if p.text)
    except Exception as e:
        logging.error(f"python-docx ile DOCX '{path}' ayrıştırılırken hata: {e}")
        return None


def parse_txt_native(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        logging.error(f"TXT '{path}' okunurken hata: {e}")
        return None


def process_file(path, use_unstructured_primarily):
    if use_unstructured_primarily:
        return parse_with_unstructured(path)
    else:
        if path.lower().endswith(".pdf"):
            return parse_pdf_pypdf(path)
        elif path.lower().endswith(".docx"):
            return parse_docx_python_docx(path)
        elif path.lower().endswith(".txt"):
            return parse_txt_native(path)
    return None


def load_documents(source_path, use_unstructured_primarily=False):
    print("[DEBUG] load_documents fonksiyonuna girildi.")
    docs = {}
    supported_extensions = (".pdf", ".docx", ".txt")

    if os.path.isdir(source_path):
        for path in glob.glob(os.path.join(source_path, "**", "*"), recursive=True):
            if os.path.isfile(path) and path.lower().endswith(supported_extensions):
                content = process_file(path, use_unstructured_primarily)
                if content:
                    docs[path] = content
    elif zipfile.is_zipfile(source_path):
        with zipfile.ZipFile(source_path, 'r') as zip_ref:
            for file_name in zip_ref.namelist():
                if file_name.lower().endswith(supported_extensions) and not file_name.endswith('/'):
                    try:
                        with zip_ref.open(file_name) as file:
                            raw_data = file.read()
                            temp_path = f"./tmp_{os.path.basename(file_name)}"
                            with open(temp_path, "wb") as temp_file:
                                temp_file.write(raw_data)
                            content = process_file(temp_path, use_unstructured_primarily)
                            os.remove(temp_path)
                            if content:
                                docs[file_name] = content
                    except Exception as e:
                        logging.error(f"{file_name} okunurken hata oluştu: {e}")
    else:
        raise ValueError("Geçerli bir klasör veya .zip dosyası giriniz.")

    return docs
