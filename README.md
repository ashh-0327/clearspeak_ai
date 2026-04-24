# ClearSpeak AI — Legal Document Simplifier

**Transform complex legal documents into clear, understandable text using AI.**

ClearSpeak AI uses advanced NLP and RAG (Retrieval-Augmented Generation) technology to analyze legal documents, identify risks, explain key terms, and generate comprehension quizzes — all in seconds.

---

## Features

- **Document Simplification** — Paste text, upload files (PDF/TXT/JPG/PNG), or capture documents via camera
- **Camera Capture** — Snap a photo of a document directly from your device
- **AI-Powered Analysis** — Summary, key terms, risk flags, action items, and overall risk level
- **Multiple Modes** — Student, Professional, and Risk Analysis
- **Comprehension Quiz** — Auto-generated quiz to test understanding
- **Domain Detection** — Automatically identifies the type of legal document
- **RAG Technology** — Retrieval-augmented generation with a curated legal knowledge base

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI (Python) |
| LLM | Llama 3.3 70B via Groq |
| RAG | ChromaDB + Sentence-Transformers |
| OCR | Tesseract OCR via PyTesseract |
| Frontend | HTML/CSS/JavaScript (Jinja2 templates) |
| PDF Parsing | pdfplumber + pdfminer |

---
Live website : https://huggingface.co/spaces/ashh-0327/Clearspeak_ai
