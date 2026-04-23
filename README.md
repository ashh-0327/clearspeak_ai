# ClearSpeak AI — Legal Document Simplifier

**Transform complex legal documents into clear, understandable text using AI.**

ClearSpeak AI uses advanced NLP and RAG (Retrieval-Augmented Generation) technology to analyze legal documents, identify risks, explain key terms, and generate comprehension quizzes — all in seconds.

---

## Features

- **📋 Document Simplification** — Paste text, upload files (PDF/TXT/JPG/PNG), or capture documents via camera
- **📸 Camera Capture** — Snap a photo of a document directly from your device
- **🧠 AI-Powered Analysis** — Summary, key terms, risk flags, action items, and overall risk level
- **📚 Multiple Modes** — Student, Professional, and Risk Analysis
- **🧩 Comprehension Quiz** — Auto-generated quiz to test understanding
- **🔍 Domain Detection** — Automatically identifies the type of legal document
- **📡 RAG Technology** — Retrieval-augmented generation with a curated legal knowledge base

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

## Project Structure

```
clearspeak-ai/
├── main.py                 # FastAPI app entry point
├── routers/
│   ├── explain.py          # /api/upload, /api/explain, /api/validate endpoints
│   └── frontend.py         # HTML page routes
├── services/
│   ├── llm.py              # Groq LLM integration
│   ├── rag.py              # ChromaDB RAG retrieval
│   ├── parser.py           # PDF/Image/Text extraction
│   ├── classifier.py       # Domain detection
│   ├── knowledge_base.py   # Legal knowledge base
│   └── validator.py        # Quiz answer validation
├── templates/
│   ├── home.html           # Landing page
│   ├── dashboard.html      # Document analysis workspace
│   ├── login.html          # Login page
│   ├── about.html          # About page
│   └── domains.html        # Domain selection page
├── static/
│   ├── css/style.css       # Design system
│   └── js/app.js           # Frontend logic
├── data/chroma_db/         # ChromaDB vector store
├── requirements.txt
├── Dockerfile
├── Procfile
├── .env                    # GROQ_API_KEY (not committed)
└── .gitignore
```

---

