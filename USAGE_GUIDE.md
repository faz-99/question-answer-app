# 📖 Complete Usage Guide

## Quick Start

### 1. First Time Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Download GPT4All model
python download_model.py

# Test the system (optional)
python test_system.py
```

### 2. Launch Application

```bash
python app.py
```

## Detailed Usage Instructions

### Loading Documents

#### Step 1: Prepare Your Documents

Supported formats:
- **PDF** (.pdf) - Textbooks, lecture notes, research papers
- **DOCX** (.docx) - Word documents, assignments
- **TXT** (.txt) - Plain text notes

**Best Practices**:
- Use clear, well-formatted documents
- Avoid scanned PDFs (OCR text works but may have errors)
- Ensure documents contain actual exam-relevant content
- Remove unnecessary headers/footers if possible

#### Step 2: Load Documents in Application

1. Open the application
2. Go to "Document Management" tab
3. Click "Load Documents" button
4. Select one or multiple files (Ctrl+Click for multiple)
5. Wait for processing (progress shown in status area)
6. Verify chunk count in the status message

**What Happens During Loading**:
- Text is extracted from each document
- Text is split into 500-character chunks with 50-character overlap
- Each chunk is converted to embeddings using SentenceTransformer
- Embeddings are stored in local ChromaDB

#### Step 3: Verify Loading

Check the status area for:
```
✅ Loading Complete!
Processed Files: 3
Total Chunks: 45
```

### Asking Questions

#### Step 1: Navigate to Q&A Tab

Click on "Question & Answer" tab

#### Step 2: Enter Your Question

Type your question in the text box. Examples:

**Good Questions** (specific, clear):
- "What is the definition of polymorphism?"
- "Explain the difference between lists and tuples"
- "Who invented Python and when?"
- "What are the main features of object-oriented programming?"

**Poor Questions** (too vague):
- "Tell me everything"
- "What is this about?"
- "Explain"

#### Step 3: Get Answer

1. Click "Get Answer" button
2. Wait for processing (usually 5-30 seconds)
3. Review the answer in the answer display area
4. Check sources at the bottom

#### Step 4: Interpret Results

**If Answer is Found**:
```
Answer: Python is a high-level programming language created by 
Guido van Rossum in 1991. It supports multiple programming paradigms...

Sources: python_basics.txt
```

**If Answer is NOT Found**:
```
Answer not found in the provided exam materials.
```

This means:
- The information is not in your loaded documents
- You may need to load additional documents
- The question may be outside the scope of your materials

### Managing Documents

#### Viewing Loaded Documents

The "Document Management" tab shows:
- Total number of chunks in database
- Processing status and history

#### Clearing Database

**When to Clear**:
- Switching to different exam/course materials
- Starting fresh with new documents
- Database becomes too large

**How to Clear**:
1. Go to "Document Management" tab
2. Click "Clear Database" button
3. Confirm the action
4. Load new documents

**⚠️ Warning**: This permanently removes all loaded documents. You'll need to reload them.

## Advanced Usage

### Optimizing for Different Document Types

#### For Short Documents (< 10 pages)

Use default settings - works well out of the box.

#### For Long Textbooks (> 100 pages)

Modify `embed_store.py`:
```python
# Line 85 - Increase chunk size
def chunk_text(self, text: str, chunk_size: int = 800, overlap: int = 100):
```

This reduces total chunks and speeds up retrieval.

#### For Technical Documents with Code

Ensure code blocks are preserved. The system handles code well in context.

### Improving Answer Quality

#### 1. Load More Relevant Documents

More context = better answers. Load all relevant course materials.

#### 2. Ask Specific Questions

Instead of: "What is Python?"
Try: "What are the three main features of Python mentioned in the course?"

#### 3. Adjust Retrieval Count

In `qa_engine.py`, line 134:
```python
# Retrieve more context chunks
def answer_question(self, question: str, top_k: int = 5):  # Changed from 3 to 5
```

More chunks = more context but slower processing.

#### 4. Adjust LLM Temperature

In `qa_engine.py`, line 109:
```python
response = self.llm.generate(
    prompt,
    max_tokens=300,
    temp=0.05,  # Lower = more factual, less creative
)
```

### Batch Question Processing

For multiple questions, you can modify the code or use the GUI repeatedly:

1. Load documents once
2. Ask first question
3. Wait for answer
4. Ask next question (documents stay loaded)

### Exporting Answers

Currently, answers are displayed in the GUI. To save answers:

1. Copy answer text from the display area
2. Paste into a text editor or Word document
3. Save for later reference

**Future Enhancement**: Add export button to save Q&A sessions.

## Troubleshooting Common Issues

### Issue: "Answer not found" for Known Information

**Possible Causes**:
1. Information is phrased differently in documents
2. Chunk size too small, splitting relevant context
3. Not enough context retrieved

**Solutions**:
- Rephrase your question to match document wording
- Increase chunk_size in embed_store.py
- Increase top_k in qa_engine.py

### Issue: Slow Answer Generation

**Causes**:
- Large model (Mistral 7B)
- Many chunks to process
- Limited CPU/RAM

**Solutions**:
- Use smaller model (orca-mini-3b)
- Reduce top_k to 2
- Close other applications
- Upgrade hardware

### Issue: Incorrect or Hallucinated Answers

**Causes**:
- LLM temperature too high
- Insufficient context
- Model generating outside context

**Solutions**:
- Lower temperature to 0.05
- Increase top_k for more context
- Check if information actually exists in documents

### Issue: Documents Not Loading

**Causes**:
- Unsupported file format
- Corrupted file
- Scanned PDF without text layer

**Solutions**:
- Convert to supported format
- Try different file
- Use OCR tool to extract text first

## Best Practices

### For Students

✅ **Do**:
- Load all relevant course materials
- Ask specific, clear questions
- Verify answers against original documents
- Use as a study aid, not a replacement for learning

❌ **Don't**:
- Rely solely on the system during exams
- Expect answers for information not in documents
- Use for plagiarism or academic dishonesty

### For Teachers/Examiners

✅ **Do**:
- Load official course materials only
- Test the system before exam use
- Monitor student usage
- Use as a reference tool

❌ **Don't**:
- Allow unsupervised access during exams
- Load external materials
- Expect 100% accuracy

### For System Administrators

✅ **Do**:
- Ensure offline environment
- Verify no internet access
- Test with sample documents
- Monitor system resources

❌ **Don't**:
- Connect to internet during use
- Share database between different courses
- Allow model modifications

## Performance Tips

### Optimize Loading Speed

1. **Use TXT files when possible** - Fastest to parse
2. **Pre-process PDFs** - Remove images, keep text only
3. **Batch load** - Load all documents at once

### Optimize Query Speed

1. **Keep database size reasonable** - Under 1000 chunks
2. **Use SSD storage** - Faster ChromaDB access
3. **Close background apps** - More RAM for LLM

### Optimize Answer Quality

1. **Load high-quality documents** - Well-formatted, clear text
2. **Use appropriate chunk size** - 500 for general, 800 for technical
3. **Adjust retrieval count** - 3-5 chunks optimal

## Security Checklist

Before using in exam environment:

- [ ] Verify no internet connection
- [ ] Check no external API calls in code
- [ ] Test with sample questions
- [ ] Verify "Answer not found" works for out-of-scope questions
- [ ] Confirm all processing is local
- [ ] Test offline functionality
- [ ] Review loaded documents
- [ ] Clear previous exam data

## FAQ

**Q: Can I use this during an exam?**
A: Only if explicitly allowed by your instructor and in a supervised environment.

**Q: Will it work without internet?**
A: Yes, completely offline after initial setup.

**Q: How accurate are the answers?**
A: Depends on document quality and question clarity. Always verify important information.

**Q: Can I load documents in other languages?**
A: Yes, but model performance may vary. English works best.

**Q: How much disk space is needed?**
A: ~10 GB (5 GB for model, 5 GB for embeddings and dependencies)

**Q: Can multiple users use it simultaneously?**
A: No, it's a single-user desktop application.

**Q: How do I update the model?**
A: Download new model, update filename in qa_engine.py

**Q: Can I use my own LLM?**
A: Yes, modify qa_engine.py to use different GPT4All models or compatible alternatives.

## Getting Help

If you encounter issues:

1. Check this guide
2. Review INSTALLATION.md
3. Run test_system.py to diagnose
4. Check error messages in terminal
5. Verify all dependencies installed

## Next Steps

- Read INSTALLATION.md for setup details
- Run test_system.py to verify installation
- Load sample documents and test
- Customize settings for your use case
