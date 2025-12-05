# 🎓 Secure Offline Exam Answer Retrieval System

A Python desktop application that answers exam questions strictly from provided course documents, with no internet access or external knowledge.

> **📑 New to this project?** Start with [INDEX.md](INDEX.md) for a complete documentation guide!

> **⚡ Want to get started quickly?** Jump to [QUICKSTART.md](QUICKSTART.md) for a 5-minute setup!

## 🛡️ Security Features

- **100% Offline**: No internet or external API calls
- **Document-Only Answers**: Strictly uses provided exam materials
- **Academic Integrity**: Returns "Answer not found" if information isn't in documents
- **Local Processing**: All embeddings and LLM inference run locally

## 📦 Tech Stack

| Component | Tool |
|-----------|------|
| GUI | PyQt5 |
| Embeddings | SentenceTransformers (all-MiniLM-L6-v2) |
| Vector Database | ChromaDB (local) |
| Local LLM | GPT4All |
| Document Parsing | pdfplumber, python-docx |

## 📁 Project Structure

```
exam-qa-system/
├── app.py              # PyQt5 GUI application
├── embed_store.py      # Document loading and embedding storage
├── qa_engine.py        # Question answering with context retrieval
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── chroma_db/         # ChromaDB storage (created automatically)
└── models/            # GPT4All model location (create this folder)
```

## 🚀 Installation

### Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Download GPT4All Model

1. Create a `models` folder in the project directory:
   ```bash
   mkdir models
   ```

2. Download the GPT4All model:
   - Visit: https://gpt4all.io/
   - Download: `ggml-gpt4all-j-v1.3-groovy.bin` (3.5 GB)
   - Alternative models:
     - `mistral-7b-openorca.Q4_0.gguf` (recommended, 3.8 GB)
     - `orca-mini-3b.ggmlv3.q4_0.bin` (smaller, 1.8 GB)

3. Place the downloaded model in the project root directory or update the path in `qa_engine.py`:
   ```python
   # In qa_engine.py, line 20
   gpt4all_model: str = "ggml-gpt4all-j-v1.3-groovy.bin"
   ```

### Step 3: Verify Installation

```bash
python -c "import PyQt5; import sentence_transformers; import chromadb; import gpt4all; print('All dependencies installed!')"
```

## 🎯 How to Run

### Start the Application

```bash
python app.py
```

### Using the Application

1. **Load Documents** (Document Management Tab):
   - Click "Load Documents"
   - Select PDF, DOCX, or TXT files containing exam materials
   - Wait for processing to complete
   - Status will show number of chunks loaded

2. **Ask Questions** (Question & Answer Tab):
   - Type your question in the text box
   - Click "Get Answer"
   - Wait for the system to search and generate answer
   - Answer and sources will be displayed

3. **Clear Database**:
   - Use "Clear Database" button to remove all loaded documents
   - Useful when switching to different exam materials

## 🔎 Answer Retrieval Logic

```
User Question
    ↓
Convert to Embeddings (SentenceTransformer)
    ↓
Retrieve Top 3 Relevant Chunks (ChromaDB)
    ↓
Pass ONLY Retrieved Text to GPT4All
    ↓
Generate Answer from Context
    ↓
If No Answer Found → "Answer not found in the provided exam materials"
```

## ⚙️ Configuration

### Adjust Chunk Size (embed_store.py)

```python
# Line 85 - Modify chunk_size for different document types
def chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 50):
```

### Adjust Retrieval Count (qa_engine.py)

```python
# Line 134 - Change top_k to retrieve more/fewer context chunks
def answer_question(self, question: str, top_k: int = 3):
```

### Change LLM Temperature (qa_engine.py)

```python
# Line 109 - Lower temp = more factual, Higher temp = more creative
response = self.llm.generate(
    prompt,
    max_tokens=300,
    temp=0.1,  # Adjust between 0.0 - 1.0
)
```

## 🧪 Testing the System

### Test with Sample Documents

1. Create a test document `test_exam.txt`:
   ```
   Python is a high-level programming language.
   It was created by Guido van Rossum in 1991.
   Python supports multiple programming paradigms.
   ```

2. Load the document in the application

3. Ask test questions:
   - "Who created Python?"
   - "When was Python created?"
   - "What is Python?" (should find answer)
   - "What is Java?" (should return "Answer not found")

## ⚠️ Troubleshooting

### Issue: "Error loading GPT4All model"

**Solution**: 
- Ensure the model file is in the correct location
- Check the filename matches exactly in `qa_engine.py`
- Verify the model file isn't corrupted (check file size)

### Issue: "No module named 'PyQt5'"

**Solution**:
```bash
pip install PyQt5==5.15.10
```

### Issue: ChromaDB errors

**Solution**:
```bash
# Delete the chroma_db folder and restart
rmdir /s /q chroma_db  # Windows
rm -rf chroma_db       # Linux
```

### Issue: Slow performance

**Solution**:
- Use smaller model (orca-mini-3b)
- Reduce chunk_size in embed_store.py
- Reduce top_k in qa_engine.py

## 🔒 Security Guarantees

✅ No internet connection required or used
✅ No external API calls (OpenAI, Claude, etc.)
✅ All processing happens locally
✅ Answers strictly from provided documents
✅ Returns "Answer not found" for out-of-scope questions

## 📋 System Requirements

- **OS**: Windows 10/11 or Linux
- **Python**: 3.8 or higher
- **RAM**: 8 GB minimum (16 GB recommended)
- **Storage**: 10 GB free space (for models and embeddings)
- **CPU**: Multi-core processor recommended

## 🎓 Academic Use Guidelines

This system is designed for:
- Study material review
- Exam preparation assistance
- Quick reference to course documents
- Teacher-supervised exam environments

**Not intended for**:
- Unsupervised exam taking
- Replacing actual learning
- Generating answers outside provided materials

## 📝 License

This project is for educational purposes. Ensure compliance with your institution's academic integrity policies.

## 🤝 Support

For issues or questions:
1. Check the Troubleshooting section
2. Verify all dependencies are installed
3. Ensure GPT4All model is downloaded correctly
4. Check that documents are in supported formats (PDF, DOCX, TXT)
