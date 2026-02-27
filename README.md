# 🧠 MediBot — Mental Health Companion

> An AI-powered mental health chatbot built with Flask, LangChain, FAISS, and LLaMA 3.1 via Groq. Answers evidence-based questions from WHO Mental Health PDFs and self-care research using Retrieval-Augmented Generation (RAG).

---

## ✨ Features

- 🔍 **RAG Pipeline** — Retrieves context from WHO PDFs + self-care CSV using FAISS vector search
- 🤖 **LLaMA 3.1 8B** — Fast, free inference via Groq API
- 🎨 **Elite Dark UI** — Animated chatbot frontend with glassmorphism and ambient glow effects
- 🔀 **Hybrid Retriever** — Combines PDF chunks + CSV self-care tips in every response
- ⚙️ **Configurable** — Adjust temperature, chunk count (k), and source visibility in sidebar
- 📚 **Source Transparency** — Every answer shows which documents it came from

---

## 🖥️ Preview

```
Sidebar                     Chat Area
┌─────────────────┐        ┌──────────────────────────────────┐
│ 🧠 MediBot      │        │  Mental Health Companion          │
│                 │        │                                  │
│ ⚙️ Settings     │        │   🧠  What is anxiety?           │
│ Temperature 0.5 │        │   👤  Anxiety is a feeling of... │
│ Chunks (k)  3   │        │       📄 Sources: who_guide.pdf  │
│ Show Sources ✓  │        │                                  │
│                 │        │  [Ask me anything...]      [➤]   │
│ ● Model Online  │        └──────────────────────────────────┘
└─────────────────┘
```

---

## 🗂️ Project Structure

```
Medical_ChatBot/
├── app.py                  # Flask backend + RAG pipeline
├── templates/
│   └── index.html          # Elite dark chatbot UI
├── vectorstore/
│   └── db_faiss/           # Pre-built FAISS index
│       ├── index.faiss
│       └── index.pkl
├── data/                   # Source documents
│   ├── who_mental_health.pdf
│   └── self_care_tips.csv
├── create_memory_for_llm.py # Script to build vectorstore
├── requirements.txt
├── Dockerfile
└── README.md
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.10+
- [Groq API Key](https://console.groq.com) (free)

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/Medical_ChatBot.git
cd Medical_ChatBot
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Environment Variable
```bash
# Windows
set HF_TOKEN=your_groq_api_key_here

# macOS/Linux
export HF_TOKEN=your_groq_api_key_here
```

### 4. Build the Vectorstore
> Skip this if `vectorstore/db_faiss/` already exists.
```bash
python create_memory_for_llm.py
```

### 5. Run the App
```bash
python app.py
```

Visit → **http://127.0.0.1:5000**

---

## 📦 Requirements

```
flask
langchain
langchain-groq
langchain-huggingface
langchain-community
faiss-cpu
sentence-transformers
torch --index-url https://download.pytorch.org/whl/cpu
```

---
### Dockerfile
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "app.py"]
```

> ⚠️ Make sure your `app.py` runs with `host="0.0.0.0"` for deployment:
> ```python
> app.run(host="0.0.0.0", port=5000, use_reloader=False)
> ```

---

## 🧠 How It Works

```
User Question
     │
     ▼
HuggingFace Embeddings
(all-MiniLM-L6-v2)
     │
     ▼
FAISS Vector Search ──── PDF Chunks
     │               └── CSV Self-care Tips (Hybrid)
     ▼
Top-k Relevant Chunks
     │
     ▼
LangChain RetrievalQA
     │
     ▼
Groq LLaMA 3.1 8B Instant
     │
     ▼
Answer + Sources → Flask API → Chat UI
```

---

## 🛠️ Configuration Options

| Setting | Default | Description |
|---|---|---|
| `temperature` | `0.5` | Response creativity (0 = factual, 1 = creative) |
| `k` | `3` | Number of document chunks retrieved |
| `show_sources` | `true` | Display source documents under each answer |
| `model` | `llama-3.1-8b-instant` | Groq-hosted LLM |
| `max_tokens` | `512` | Maximum response length |
| `embedding_model` | `all-MiniLM-L6-v2` | HuggingFace sentence transformer |

---

## ⚠️ Common Issues

| Problem | Fix |
|---|---|
| `Connection failed` error | Add `use_reloader=False` to `app.run()` |
| Vectorstore not found | Run `python create_memory_for_llm.py` first |
| Slow first response | Model loading takes ~20s on first request |
| Render cold start delay | Free tier sleeps after 15 min of inactivity |
| CUDA/GPU errors | Use `faiss-cpu` instead of `faiss-gpu` |

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

## 🙌 Acknowledgements

- [WHO Mental Health Resources](https://www.who.int/health-topics/mental-health)
- [Groq](https://groq.com) — Fast LLM inference
- [LangChain](https://langchain.com) — RAG framework
- [FAISS](https://github.com/facebookresearch/faiss) — Facebook AI Similarity Search
- [HuggingFace](https://huggingface.co) — Embedding models

---

  Built with ❤️ for mental health awareness
