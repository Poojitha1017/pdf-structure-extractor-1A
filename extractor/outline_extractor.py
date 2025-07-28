import pytesseract
from PIL import Image
import numpy as np

def get_outline(doc):
    from collections import Counter

    font_sizes = []
    elements = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        blocks = page.get_text("dict")["blocks"]

        if not any(b.get("lines") for b in blocks):
            # OCR fallback for image-based page
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            ocr_text = pytesseract.image_to_string(img)
            lines = ocr_text.split("\n")
            for line in lines:
                line = line.strip()
                if len(line.split()) >= 3 and line.isupper():
                    elements.append({
                        "text": line,
                        "font_size": 16,  # Assume mid-level heading
                        "font_name": "OCR",
                        "page": page_num + 1,
                        "y": 0  # we can’t know y from image, default top
                    })
            continue

        # Extract normal text-based headings
        for block in blocks:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                for span in line["spans"]:
                    text = span["text"].strip()
                    if not text or len(text) < 5:
                        continue
                    font_size = round(span["size"])
                    font_name = span["font"]
                    bbox = span.get("bbox", [0, 0, 0, 0])
                    y_pos = bbox[1]  # y-coordinate

                    elements.append({
                        "text": text,
                        "font_size": font_size,
                        "font_name": font_name,
                        "page": page_num + 1,
                        "y": y_pos
                    })
                    font_sizes.append(font_size)

    if not elements:
        return []

    # Determine top font sizes
    font_freq = Counter(font_sizes)
    common_sizes = sorted(font_freq.keys(), reverse=True)
    size_to_level = {}

    if len(common_sizes) >= 1:
        size_to_level[common_sizes[0]] = "H1"
    if len(common_sizes) >= 2:
        size_to_level[common_sizes[1]] = "H2"
    if len(common_sizes) >= 3:
        size_to_level[common_sizes[2]] = "H3"

    outline = []
    seen = set()

    for el in elements:
        text = el["text"]
        page = el["page"]
        font_size = el["font_size"]
        y = el["y"]

        if el["font_name"] == "OCR":
            level = "H2" if len(text.split()) > 4 else "H3"
        else:
            level = size_to_level.get(font_size)

        if not level:
            continue

        # Boost headings near top of page
        if y <= 150 and level == "H3":
            level = "H2"

        key = (text.lower(), page)
        if key in seen:
            continue
        seen.add(key)

        outline.append({
            "level": level,
            "text": text,
            "page": page
        })

    return outline
