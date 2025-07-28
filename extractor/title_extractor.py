import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import re

def preprocess_image_for_ocr(image):
    """Convert to grayscale and apply thresholding for better OCR accuracy."""
    gray = image.convert("L")
    bw = gray.point(lambda x: 0 if x < 160 else 255, '1')
    return bw

def extract_title_from_first_page(doc):
    page = doc[0]
    blacklist = ["oceanofpdf", ".com", "copyright", "http", "www.", "all rights reserved"]
    best_candidate = {"text": "", "score": 0}

    # Extract vector text
    blocks = page.get_text("dict")["blocks"]
    has_text = any("lines" in block and block["lines"] for block in blocks)

    if has_text:
        for block in blocks:
            for line in block.get("lines", []):
                for span in line["spans"]:
                    text = span["text"].strip()
                    if not text or len(text) < 4:
                        continue
                    if any(b in text.lower() for b in blacklist):
                        continue

                    font_size = span["size"]
                    font_name = span["font"]
                    is_bold = "Bold" in font_name
                    is_all_caps = text.isupper()
                    y = span.get("bbox", [0, 0, 0, 0])[1]

                    score = font_size + (3 if is_bold else 0) + (2 if is_all_caps else 0) + max(0, 50 - y / 10)

                    if score > best_candidate["score"]:
                        best_candidate = {
                            "text": text,
                            "score": score
                        }

    else:
        # Fallback to OCR
        pix = page.get_pixmap(dpi=300)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        preprocessed = preprocess_image_for_ocr(img)

        ocr_data = pytesseract.image_to_data(preprocessed, output_type=pytesseract.Output.DICT)
        n_boxes = len(ocr_data['level'])
        candidates = []

        for i in range(n_boxes):
            text = ocr_data['text'][i].strip()
            if not text or len(text) < 2:
                continue
            if any(b in text.lower() for b in blacklist):
                continue

            x, y, w, h = (ocr_data['left'][i], ocr_data['top'][i],
                          ocr_data['width'][i], ocr_data['height'][i])
            is_all_caps = text.isupper()
            score = h + (10 if is_all_caps else 0) + max(0, 50 - y / 10)

            candidates.append({
                "text": text,
                "score": score,
                "y": y,
                "x": x,
                "height": h
            })

        # Combine top lines (assume title is multi-line & boldest)
        if candidates:
            candidates.sort(key=lambda c: (-c["score"], c["y"], c["x"]))
            top_y = candidates[0]["y"]
            top_lines = [c for c in candidates if abs(c["y"] - top_y) <= 30]

            # Sort horizontally and join
            top_lines.sort(key=lambda c: c["x"])
            title_text = " ".join([c["text"] for c in top_lines])

            # Check next line if aligned vertically
            next_line_y = top_y + top_lines[0]["height"] + 5
            second_line = [c for c in candidates if abs(c["y"] - next_line_y) <= 30]
            second_line.sort(key=lambda c: c["x"])
            if second_line:
                title_text += " " + " ".join([c["text"] for c in second_line])

            best_candidate["text"] = title_text.strip()

    return best_candidate["text"] if best_candidate["text"] else "Unknown Title"
