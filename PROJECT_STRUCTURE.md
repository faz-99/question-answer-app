# 📁 Project Structure Documentation

## Overview

This document explains the architecture and file organization of the Offline Exam Answer Retrieval System.

## Directory Structure

```
exam-qa-system/
│
├── Core Application Files
│   ├── app.py                    # Main PyQt5 GUI application
│   ├── embed_store.py            # Document loading and embedding storage
│   ├── qa_engine.py              # Question answering engine
│   └── requirements.txt          # Python dependencies
│
├── Documentation
│   ├── README.md                 # Project overview and main documentation
│   ├── INSTALLATION.md           # Detailed installation instructions
│   ├── USAGE_GUIDE.md            # Complete usage instructions
│   ├── QUICKSTART.md             # Quick start guide
│   └── PROJECT_STRUCTURE.md      # This file
│
├── Utility Scripts
│   ├── download_model.py         # GPT4All model downloader
│   └── test_system.py            # System testing script
│
├── Configuration
│   └── .gitignore                # Git ignore rules
│
└── Generated/Runtime Directories (created automatically)
    ├── chroma_db/                # ChromaDB vector database storage
    ├── __pycache__/              # Python bytecode cache
    └── venv/                     # Virtual environment (if created)
```

## Core Components

### 1. app.py - GUI Application

**Purpose**: Main user interface using PyQt5

**Key Classes**:
- `ExamQAApp`: Main application window
- `DocumentLoadThread`: Background thread for document loading
- `QAThread`: Background thread for question answering

**Features**:
- Tab-based interface (Document Management, Q&A)
- Non-blocking operations using threads
- Real-time status updates
- File selection dialogs
- Answer and source display

**Dependencies**:
- PyQt5 (GUI framework)
- embed_store.DocumentStore
- qa_engine.QAEngine

**Entry Point**: `main()` function

### 2. embed_store.py - Document Processing

**Purpose**: Handle document loading, text extraction, and embedding storage

**Key Class**: `DocumentStore`

**Methods**:
```python
__init__(db_path, model_name)           # Initialize store
extract_text(file_path)                 # Extract text from any supported format
extract_text_from_pdf(file_path)        # PDF-specific extraction
extract_text_from_docx(file_path)       # DOCX-specific extraction
extract_text_from_txt(file_path)        # TXT-specific extraction
chunk_text(text, chunk_size, overlap)   # Split text into chunks
load_documents(file_paths)              # Load and process multiple documents
clear_database()                        # Clear all stored documents
get_collection_count()                  # Get number of stored chunks
```

**Dependencies**:
- pdfplumber (PDF parsing)
- python-docx (DOCX parsing)
- sentence-transformers (embeddings)
- chromadb (vector storage)

**Configuration**:
- Default chunk size: 500 characters
- Default overlap: 50 characters
- Embedding model: all-MiniLM-L6-v2

### 3. qa_engine.py - Question Answering

**Purpose**: Retrieve relevant context and generate answers using LLM

**Key Class**: `QAEngine`

**Methods**:
```python
__init__(db_path, model_name, gpt4all_model)  # Initialize engine
_load_llm()                                    # Load GPT4All model
retrieve_context(question, top_k)              # Get relevant chunks
generate_answer(question, contexts)            # Generate answer from context
answer_question(question, top_k)               # Complete QA pipeline
```

**Pipeline**:
1. Convert question to embedding
2. Query ChromaDB for similar chunks
3. Retrieve top-k most relevant chunks
4. Create prompt with context
5. Generate answer using GPT4All
6. Return answer with sources

**Dependencies**:
- sentence-transformers (question embeddings)
- chromadb (vector search)
- gpt4all (local LLM)

**Configuration**:
- Default top_k: 3 chunks
- LLM temperature: 0.1 (factual)
- Max tokens: 300

## Data Flow

### Document Loading Flow

```
User selects files
    ↓
app.py: DocumentLoadThread
    ↓
embed_store.py: load_documents()
    ↓
For each file:
    extract_text() → chunk_text() → generate embeddings
    ↓
Store in ChromaDB
    ↓
Return statistics
    ↓
Update GUI
```

### Question Answering Flow

```
User enters question
    ↓
app.py: QAThread
    ↓
qa_engine.py: answer_question()
    ↓
retrieve_context()
    ├─ Convert question to embedding
    ├─ Query ChromaDB
    └─ Return top-k chunks
    ↓
generate_answer()
    ├─ Create prompt with context
    ├─ Call GPT4All
    └─ Return answer
    ↓
Display in GUI with sources
```

## Database Schema

### ChromaDB Collection: "exam_documents"

**Fields**:
- `id`: Unique identifier (file_hash + chunk_index)
- `embedding`: 384-dimensional vector (from all-MiniLM-L6-v2)
- `document`: Text content of chunk
- `metadata`: 
  - `source`: Original filename

**Index**: HNSW (Hierarchical Navigable Small World) with cosine similarity

## Configuration Files

### requirements.txt

Lists all Python dependencies with versions:
- PyQt5==5.15.10 (GUI)
- sentence-transformers==2.2.2 (embeddings)
- chromadb==0.4.22 (vector DB)
- gpt4all==2.0.2 (local LLM)
- pdfplumber==0.10.3 (PDF parsing)
- python-docx==1.1.0 (DOCX parsing)
- torch==2.1.2 (ML backend)

### .gitignore

Excludes from version control:
- Python cache files
- Virtual environments
- ChromaDB data
- Model files
- IDE configurations

## Utility Scripts

### download_model.py

**Purpose**: Download GPT4All model automatically

**Usage**:
```bash
python download_model.py
```

**What it does**:
1. Imports GPT4All
2. Triggers model download
3. Shows progress
4. Confirms success

### test_system.py

**Purpose**: Comprehensive system testing

**Tests**:
1. Document loading
2. Context retrieval
3. Question answering (optional)

**Usage**:
```bash
python test_system.py
```

## Extension Points

### Adding New Document Formats

In `embed_store.py`, add new extraction method:

```python
def extract_text_from_newformat(self, file_path: str) -> str:
    # Your extraction logic
    return text

# Update extract_text() method
def extract_text(self, file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.newformat':
        return self.extract_text_from_newformat(file_path)
    # ... existing code
```

### Using Different LLM Models

In `qa_engine.py`, modify `__init__`:

```python
def __init__(self, ..., gpt4all_model: str = "your-model.gguf"):
    # Model will be loaded automatically
```

### Customizing Chunk Strategy

In `embed_store.py`, modify `chunk_text()`:

```python
def chunk_text(self, text: str, chunk_size: int = 800, overlap: int = 100):
    # Your custom chunking logic
```

### Adding Export Functionality

In `app.py`, add export button and method:

```python
def export_answer(self):
    answer = self.answer_display.toPlainText()
    file_path, _ = QFileDialog.getSaveFileName(self, "Export Answer", "", "Text Files (*.txt)")
    if file_path:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(answer)
```

## Security Considerations

### Offline Enforcement

**Current Implementation**:
- No network imports in code
- All models run locally
- ChromaDB in local mode

**To Verify**:
```python
# Check no requests/urllib in imports
grep -r "import requests" *.py
grep -r "import urllib" *.py
```

### Data Isolation

- Each course should use separate `chroma_db` directory
- Clear database between different exams
- No data sharing between sessions

### Academic Integrity

- System only answers from provided documents
- Returns "Answer not found" for external knowledge
- All processing is transparent and auditable

## Performance Optimization

### Memory Usage

**Typical Usage**:
- Base application: ~500 MB
- Embedding model: ~100 MB
- GPT4All model: ~4 GB (loaded in RAM)
- ChromaDB: ~10 MB per 1000 chunks

**Total**: ~5-6 GB RAM minimum

### Speed Optimization

**Document Loading**:
- Parallel processing: Not implemented (can be added)
- Batch embedding: Already implemented
- Caching: ChromaDB handles this

**Question Answering**:
- Embedding cache: SentenceTransformer caches
- LLM optimization: Use smaller models
- Context limit: Reduce top_k

## Troubleshooting Guide

### Common Issues and Solutions

| Issue | File | Solution |
|-------|------|----------|
| Model not loading | qa_engine.py | Check model path, re-download |
| Slow embedding | embed_store.py | Use GPU if available |
| Poor answers | qa_engine.py | Increase top_k, lower temperature |
| Memory errors | app.py | Use smaller model, reduce chunk size |
| ChromaDB errors | embed_store.py | Delete chroma_db folder, restart |

## Development Workflow

### Adding New Features

1. **Plan**: Document the feature
2. **Implement**: Add code to appropriate module
3. **Test**: Use test_system.py or create new tests
4. **Document**: Update relevant .md files
5. **Verify**: Test in GUI

### Testing Changes

```bash
# Test document loading
python -c "from embed_store import DocumentStore; ds = DocumentStore(); print('OK')"

# Test QA engine
python -c "from qa_engine import QAEngine; qa = QAEngine(); print('OK')"

# Full system test
python test_system.py
```

## Future Enhancements

Potential additions (not implemented):

1. **Multi-language support**: Add translation layer
2. **Answer export**: Save Q&A sessions
3. **Batch processing**: Process multiple questions
4. **Answer confidence**: Show confidence scores
5. **Document preview**: View loaded documents
6. **Search history**: Track previous questions
7. **Admin panel**: Teacher controls
8. **Time-lock**: Restrict access by time
9. **Plagiarism detection**: Check for hallucinations
10. **MCQ auto-grader**: Automated grading

## Maintenance

### Regular Tasks

- Update dependencies: `pip install --upgrade -r requirements.txt`
- Clear old databases: Delete `chroma_db/` folder
- Update models: Download newer GPT4All models
- Backup important documents: Copy source files

### Monitoring

- Check disk space (ChromaDB grows with documents)
- Monitor RAM usage (LLM can be memory-intensive)
- Review answer quality periodically
- Test with new document types

## License and Credits

**Dependencies**:
- PyQt5: GPL/Commercial
- SentenceTransformers: Apache 2.0
- ChromaDB: Apache 2.0
- GPT4All: MIT
- pdfplumber: MIT
- python-docx: MIT

**Project**: Educational use, ensure compliance with academic policies.
