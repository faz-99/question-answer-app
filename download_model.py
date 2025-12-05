"""
Helper script to download GPT4All model.
Run this once after installing dependencies.
"""

from gpt4all import GPT4All
import os

def download_model():
    """Download the default GPT4All model."""
    print("=" * 60)
    print("GPT4All Model Downloader")
    print("=" * 60)
    print("\nThis will download the GPT4All model (~3.5 GB)")
    print("The download may take several minutes depending on your connection.\n")
    
    model_name = "ggml-gpt4all-j-v1.3-groovy.bin"
    
    try:
        print(f"Downloading: {model_name}")
        print("Please wait...\n")
        
        model = GPT4All(model_name)
        
        print("\n" + "=" * 60)
        print("✅ Model downloaded successfully!")
        print("=" * 60)
        print(f"\nModel location: {model.config['model_path']}")
        print("\nYou can now run the application with: python app.py")
        
    except Exception as e:
        print("\n" + "=" * 60)
        print("❌ Error downloading model")
        print("=" * 60)
        print(f"\nError: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Check your internet connection")
        print("2. Try downloading manually from: https://gpt4all.io/")
        print("3. Place the model file in: ~/.cache/gpt4all/")

if __name__ == "__main__":
    download_model()
