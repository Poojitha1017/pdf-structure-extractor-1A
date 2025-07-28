# 🧠 PDF Structure Extractor – Challenge 1A Submission

This project extracts a **structured outline** (H1, H2, H3) and the **boldest title** from the first page of each PDF in the `input` folder. It works completely **offline inside a Docker container** and supports **multilingual documents** (e.g., English, Hindi).

---

## 🧩 Approach

### 🏷️ Title Extraction

- Extracts the **boldest, largest-font text** from the first page.
- Uses `PyMuPDF` for text-based PDFs.
- Falls back to `Tesseract OCR` for scanned/image-based PDFs.
- Merges top-aligned words (even split across lines) as title.
- Filters out unwanted watermarks, URLs, and boilerplate text.

### 🗂️ Outline Extraction

- Extracts section headings across all pages using `PyMuPDF`.
- Dynamically groups headings into `H1`, `H2`, and `H3` levels based on font size and positioning.
- Handles noisy and unstructured documents robustly.

---

## 🔧 Dependencies / Libraries Used

All dependencies are installed within the Docker container using `.whl` and `.deb` files:

- [`PyMuPDF`](https://github.com/pymupdf/PyMuPDF) – PDF text extraction
- [`pytesseract`](https://github.com/madmaze/pytesseract) – OCR for scanned pages
- [`Pillow`](https://python-pillow.org/) – image handling
- [`packaging`](https://pypi.org/project/packaging/) – font size comparison

> Offline installation is supported via bundled `.whl` and `.deb` files.

---

## 📦 How to Build & Run

You do **not need to install anything locally** – everything runs in Docker.

---

### 🐳 Build Docker Image

#### 🐧 Unix / macOS

```bash
docker build --platform linux/amd64 -t docparser:1a .

Windows PowerShell:
docker build --platform linux/amd64 -t docparser:1a .

Run the Container:

Unix / macOS:
docker run --rm -v ${PWD}/input:/app/input -v ${PWD}/output:/app/output --network none docparser:1a

Windows PowerShell:
docker run --rm -v "${PWD}\input:/app/input" -v "${PWD}\output:/app/output" --network none docparser:1a


This **strengthens your submission** and avoids last-minute issues across different machines. You're on the right track — just push with this included. 💪🚀

