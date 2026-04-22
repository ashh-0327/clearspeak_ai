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

## Setup (Local)

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/clearspeak-ai.git
cd clearspeak-ai

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/Mac

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
# Create a .env file with:
# GROQ_API_KEY=your_groq_api_key_here

# 5. Run the server
uvicorn main:app --reload --port 8000
```

Visit **http://localhost:8000**

---

## Deployment

### Docker

```bash
docker build -t clearspeak-ai .
docker run -p 8000:8000 --env-file .env clearspeak-ai
```

### Render

1. Push to GitHub
2. Create a new **Web Service** on [Render](https://render.com)
3. Select **Docker** as the environment
4. Add environment variable: `GROQ_API_KEY`
5. Deploy

### Railway

1. Push to GitHub
2. Create a new project on [Railway](https://railway.app)
3. Connect your GitHub repo
4. Add environment variable: `GROQ_API_KEY`
5. Railway auto-detects the Dockerfile and deploys

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Landing page |
| GET | `/dashboard` | Document analysis workspace |
| GET | `/login` | Login page |
| GET | `/about` | About page |
| POST | `/api/upload` | Upload & extract text from a file |
| POST | `/api/explain` | Upload a file and get full AI analysis |
| POST | `/api/validate` | Validate quiz answers |
| GET | `/api/ping` | Health check |
| GET | `/docs` | Swagger API docs |

---

## Environment Variables

| Variable | Description |
|----------|-------------|
| `GROQ_API_KEY` | API key from [Groq Console](https://console.groq.com) |

---

## License

This project is for educational and demonstration purposes.

---

*Built with ❤️ using FastAPI, Groq, and ChromaDB*
