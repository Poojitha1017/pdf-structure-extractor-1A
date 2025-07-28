from extractor.title_extractor import extract_title_from_first_page
from extractor.outline_extractor import get_outline
from utils.io_utils import save_json, get_pdf_paths
import fitz  # PyMuPDF
import os

def process_pdf(file_path):
    try:
        doc = fitz.open(file_path)
        title = extract_title_from_first_page(doc)
        outline = get_outline(doc)
        save_json(file_path, title, outline)
    except Exception as e:
        print(f"[❌] Failed to process {file_path}: {e}")

def main():
    input_dir = "input"
    os.makedirs("output", exist_ok=True)
    pdf_files = get_pdf_paths(input_dir)

    for file_path in pdf_files:
        process_pdf(file_path)

if __name__ == "__main__":
    main()
