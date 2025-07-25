import argparse
import gradio as gr
import sys
import traceback
import os
from app.pipeline import autorag_process


# --- CLI Modu ---
def cli_main():
    parser = argparse.ArgumentParser(description="AutoRAG - Terminal Kullanımı")
    parser.add_argument("--file", required=True, help=".zip dosyasının yolu")
    parser.add_argument("--query", required=True, help="Sorulacak soru")
    parser.add_argument("--embed", default="sentence-transformers/distiluse-base-multilingual-cased-v1", help="Embedding modeli")
    parser.add_argument("--llm", default="mistral:instruct", help="LLM modeli")
    parser.add_argument("--topk", type=int, default=3, help="Top-K chunk sayısı")

    args = parser.parse_args()

    print("AutoRAG başlatılıyor...\n")
    answer = autorag_process(
        zip_file_path=args.file,
        question=args.query,
        top_k_size=args.topk,
        embedding_model=args.embed,
        llm_model=args.llm,
        collection_name=os.path.splitext(os.path.basename(args.file))[0]
    )
    print("Yanıt:\n", answer)


# --- GUI Modu ---
def gui_main():
    def gui_handler(file, question, top_k_size, embedding_model, llm_model):
        if file is None or not question.strip():
            return "Lütfen geçerli bir dosya ve soru girin."


        try:
            return autorag_process(
                    zip_file_path=file.name,
                    question=question,
                    top_k_size=int(top_k_size),
                    embedding_model=embedding_model,
                    llm_model=llm_model,
                    collection_name=os.path.splitext(os.path.basename(file.name))[0]
            )
        except Exception as e:
            print("\n--- HATA: AutoRAG çalıştırılırken bir istisna oluştu ---")
            traceback.print_exc()  # Tüm detaylı hata terminale
            return f"Hata oluştu: {e}" 

    with gr.Blocks(title="AutoRAG",theme=gr.themes.Base()) as demo:
        gr.Markdown("## AutoRAG")

        with gr.Row():
            file_input = gr.File(
                label="📄 Belge Yükle (.pdf, .docx, .txt, .md, .zip)",
                file_types=[".pdf", ".docx", ".txt", ".md", ".zip"]
            )

        with gr.Row():
            embedding_model = gr.Dropdown(
                choices=[
                    "sentence-transformers/distiluse-base-multilingual-cased-v1",
                    "sentence-transformers/distiluse-base-multilingual-cased-v2",
                ],
                label="Embedding Modeli",
                value="sentence-transformers/distiluse-base-multilingual-cased-v1"
            )
            llm_model = gr.Dropdown(
                choices=[
                    "mistral:instruct",
                    "gemma:2b",
                    "Phi-2"
                ],
                label="LLM Modeli",
                value="mistral:instruct"
            )

        with gr.Row():
            top_k_size = gr.Slider(
                minimum=1, maximum=10, step=1, value=3,
                label="Top-K (kaç chunk alınsın?)"
            )
            question = gr.Textbox(
                label="Soru",
                placeholder="Örn: Bu belge ne anlatıyor?",
                lines=2
            )

        run_btn = gr.Button("Çalıştır")
        output = gr.Textbox(label="Yanıt", lines=10, interactive=False)

        run_btn.click(
            fn=gui_handler,
            inputs=[file_input, question, top_k_size, embedding_model, llm_model],
            outputs=output
        )
    port=7860
    url = f"http://localhost:{port}"
    print("Enter this link to open:",url)
    demo.launch(server_name="0.0.0.0", server_port=7860)
    

# --- Giriş noktası ---
if __name__ == "__main__":
    if len(sys.argv) > 1:
        cli_main()
    else:
        gui_main()
