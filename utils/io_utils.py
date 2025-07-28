import os
import json

def save_json(input_path, title, outline):
    base_name = os.path.splitext(os.path.basename(input_path))[0]
    output_path = f"output/{base_name}.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump({
            "title": title,
            "outline": outline
        }, f, indent=2, ensure_ascii=False)
    print(f"[✅] Saved: {output_path}")

def get_pdf_paths(input_dir):
    return [
        os.path.join(input_dir, file)
        for file in os.listdir(input_dir)
        if file.endswith(".pdf")
    ]