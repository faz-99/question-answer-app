# 📦 Detailed Installation Guide

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- 10 GB free disk space
- Internet connection (for initial setup only)

## Step-by-Step Installation

### For Windows

#### 1. Install Python

```cmd
# Download Python from https://www.python.org/downloads/
# During installation, check "Add Python to PATH"

# Verify installation
python --version
pip --version
```

#### 2. Create Project Directory

```cmd
mkdir exam-qa-system
cd exam-qa-system
```

#### 3. Create Virtual Environment (Recommended)

```cmd
python -m venv venv
venv\Scripts\activate
```

#### 4. Install Dependencies

```cmd
pip install -r requirements.txt
```

**Note**: This may take 10-15 minutes as it downloads PyTorch and other large packages.

#### 5. Download GPT4All Model

**Option A: Using Python Script**

Create `download_model.py`:

```python
from gpt4all import GPT4All

# This will download the model automatically
model = GPT4All("ggml-gpt4all-j-v1.3-groovy.bin")
print("Model downloaded successfully!")
```

Run:
```cmd
python download_model.py
```

**Option B: Manual Download**

1. Visit: https://gpt4all.io/models/ggml-gpt4all-j-v1.3-groovy.bin
2. Download the file (3.5 GB)
3. Place it in: `C:\Users\<YourUsername>\.cache\gpt4all\`

#### 6. Verify Installation

```cmd
python -c "import PyQt5; import sentence_transformers; import chromadb; import gpt4all; print('✅ All dependencies installed!')"
```

#### 7. Run the Application

```cmd
python app.py
```

---

### For Linux (Ubuntu/Debian)

#### 1. Install Python and Dependencies

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
sudo apt install python3-pyqt5  # Optional: system PyQt5
```

#### 2. Create Project Directory

```bash
mkdir exam-qa-system
cd exam-qa-system
```

#### 3. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

#### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 5. Download GPT4All Model

```bash
# Create download script
cat > download_model.py << 'EOF'
from gpt4all import GPT4All
model = GPT4All("ggml-gpt4all-j-v1.3-groovy.bin")
print("Model downloaded successfully!")
EOF

python download_model.py
```

#### 6. Verify Installation

```bash
python -c "import PyQt5; import sentence_transformers; import chromadb; import gpt4all; print('✅ All dependencies installed!')"
```

#### 7. Run the Application

```bash
python app.py
```

---

## Alternative Models

If you want to use a different GPT4All model:

### Recommended Models

1. **Mistral 7B OpenOrca** (Best quality, 3.8 GB)
   ```python
   # In qa_engine.py, change line 20 to:
   gpt4all_model: str = "mistral-7b-openorca.Q4_0.gguf"
   ```

2. **Orca Mini 3B** (Faster, smaller, 1.8 GB)
   ```python
   gpt4all_model: str = "orca-mini-3b.ggmlv3.q4_0.bin"
   ```

3. **GPT4All Falcon** (Balanced, 4 GB)
   ```python
   gpt4all_model: str = "gpt4all-falcon-q4_0.gguf"
   ```

### Download Alternative Models

```python
from gpt4all import GPT4All

# Download specific model
model = GPT4All("mistral-7b-openorca.Q4_0.gguf")
```

---

## Troubleshooting Installation

### Issue: pip install fails with "No matching distribution"

**Solution**:
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Try again
pip install -r requirements.txt
```

### Issue: PyQt5 installation fails on Linux

**Solution**:
```bash
# Install system dependencies
sudo apt install python3-pyqt5 python3-pyqt5.qtwidgets

# Or use conda
conda install pyqt
```

### Issue: Torch installation is slow or fails

**Solution**:
```bash
# Install CPU-only version (smaller, faster)
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

### Issue: ChromaDB errors on Windows

**Solution**:
```cmd
# Install Visual C++ Build Tools
# Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/

# Then reinstall chromadb
pip uninstall chromadb
pip install chromadb
```

### Issue: GPT4All model not found

**Solution**:
```python
# Check model location
import os
from pathlib import Path

cache_dir = Path.home() / ".cache" / "gpt4all"
print(f"Models should be in: {cache_dir}")
print(f"Files found: {list(cache_dir.glob('*.bin'))}")
```

---

## Offline Installation

If you need to install on a machine without internet:

### 1. Download Dependencies on Internet-Connected Machine

```bash
# Create requirements directory
mkdir offline_packages
cd offline_packages

# Download all packages
pip download -r requirements.txt

# Download model manually from https://gpt4all.io/
```

### 2. Transfer to Offline Machine

Copy the `offline_packages` folder and model file to the offline machine.

### 3. Install on Offline Machine

```bash
# Install from local packages
pip install --no-index --find-links=offline_packages -r requirements.txt

# Place model in cache directory
mkdir -p ~/.cache/gpt4all/
cp ggml-gpt4all-j-v1.3-groovy.bin ~/.cache/gpt4all/
```

---

## Verifying Complete Installation

Run this comprehensive check:

```python
# save as check_installation.py
import sys

def check_installation():
    checks = []
    
    # Check Python version
    py_version = sys.version_info
    checks.append(("Python Version", f"{py_version.major}.{py_version.minor}.{py_version.micro}", 
                   py_version >= (3, 8)))
    
    # Check imports
    try:
        import PyQt5
        checks.append(("PyQt5", PyQt5.QtCore.PYQT_VERSION_STR, True))
    except ImportError as e:
        checks.append(("PyQt5", str(e), False))
    
    try:
        import sentence_transformers
        checks.append(("SentenceTransformers", sentence_transformers.__version__, True))
    except ImportError as e:
        checks.append(("SentenceTransformers", str(e), False))
    
    try:
        import chromadb
        checks.append(("ChromaDB", chromadb.__version__, True))
    except ImportError as e:
        checks.append(("ChromaDB", str(e), False))
    
    try:
        import gpt4all
        checks.append(("GPT4All", gpt4all.__version__, True))
    except ImportError as e:
        checks.append(("GPT4All", str(e), False))
    
    try:
        import pdfplumber
        checks.append(("pdfplumber", pdfplumber.__version__, True))
    except ImportError as e:
        checks.append(("pdfplumber", str(e), False))
    
    try:
        from docx import Document
        checks.append(("python-docx", "OK", True))
    except ImportError as e:
        checks.append(("python-docx", str(e), False))
    
    # Print results
    print("\n" + "="*60)
    print("INSTALLATION CHECK RESULTS")
    print("="*60)
    
    for name, version, status in checks:
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {name:25} {version}")
    
    print("="*60)
    
    all_ok = all(check[2] for check in checks)
    if all_ok:
        print("\n🎉 All dependencies installed successfully!")
        print("You can now run: python app.py")
    else:
        print("\n⚠️  Some dependencies are missing. Please install them.")
    
    return all_ok

if __name__ == "__main__":
    check_installation()
```

Run:
```bash
python check_installation.py
```

---

## Next Steps

After successful installation:

1. ✅ Run `python app.py` to start the application
2. ✅ Load sample documents to test
3. ✅ Ask test questions
4. ✅ Review the README.md for usage guidelines

## Getting Help

If you encounter issues not covered here:

1. Check Python version: `python --version` (must be 3.8+)
2. Check pip version: `pip --version`
3. Try reinstalling in a fresh virtual environment
4. Check system requirements (8GB RAM minimum)
