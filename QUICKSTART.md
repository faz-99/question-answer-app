# ⚡ Quick Start Guide

Get up and running in 5 minutes!

## Prerequisites

- Python 3.8+ installed
- 10 GB free disk space
- Internet (for initial setup only)

## Installation (3 steps)

### Step 1: Install Dependencies (5-10 minutes)

```bash
pip install -r requirements.txt
```

### Step 2: Download Model (5-10 minutes)

```bash
python download_model.py
```

### Step 3: Run Application

```bash
python app.py
```

## First Use (2 minutes)

### 1. Load a Test Document

Create `test.txt`:
```
Python is a programming language created by Guido van Rossum in 1991.
It is known for its simplicity and readability.
Python is used in web development, data science, and automation.
```

### 2. Load in Application

- Click "Load Documents"
- Select `test.txt`
- Wait for "Loading Complete"

### 3. Ask a Question

- Go to "Question & Answer" tab
- Type: "Who created Python?"
- Click "Get Answer"
- See result!

## Expected Result

```
Answer: Python was created by Guido van Rossum in 1991.

Sources: test.txt
```

## What's Next?

- Load your actual exam documents (PDF, DOCX, TXT)
- Ask real questions
- Read USAGE_GUIDE.md for advanced features

## Troubleshooting

### "Error loading GPT4All model"
→ Run `python download_model.py` again

### "No module named 'PyQt5'"
→ Run `pip install PyQt5`

### Slow performance
→ Use smaller model: edit `qa_engine.py` line 20 to `"orca-mini-3b.ggmlv3.q4_0.bin"`

## Need Help?

- Full installation guide: `INSTALLATION.md`
- Detailed usage: `USAGE_GUIDE.md`
- Test system: `python test_system.py`
