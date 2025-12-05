"""
Test script to verify the exam QA system is working correctly.
Creates sample documents and tests the QA pipeline.
"""

import os
import tempfile
from embed_store import DocumentStore
from qa_engine import QAEngine

def create_test_documents():
    """Create sample test documents."""
    temp_dir = tempfile.mkdtemp()
    
    # Create test TXT file
    txt_path = os.path.join(temp_dir, "python_basics.txt")
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write("""
Python Programming Language

Python is a high-level, interpreted programming language created by Guido van Rossum.
It was first released in 1991.

Key Features:
- Easy to learn and read
- Supports multiple programming paradigms (object-oriented, functional, procedural)
- Has a large standard library
- Cross-platform compatibility

Python is widely used in:
- Web development (Django, Flask)
- Data science and machine learning
- Automation and scripting
- Scientific computing

Popular Python frameworks include Django for web development and TensorFlow for machine learning.
        """)
    
    # Create another test file
    txt_path2 = os.path.join(temp_dir, "data_structures.txt")
    with open(txt_path2, 'w', encoding='utf-8') as f:
        f.write("""
Data Structures in Python

Lists:
Lists are ordered, mutable collections. They can contain elements of different types.
Example: my_list = [1, 2, 3, "hello"]

Dictionaries:
Dictionaries store key-value pairs. They are unordered and mutable.
Example: my_dict = {"name": "John", "age": 30}

Tuples:
Tuples are ordered, immutable collections.
Example: my_tuple = (1, 2, 3)

Sets:
Sets are unordered collections of unique elements.
Example: my_set = {1, 2, 3}
        """)
    
    return [txt_path, txt_path2]

def test_document_loading():
    """Test document loading and embedding."""
    print("\n" + "="*60)
    print("TEST 1: Document Loading")
    print("="*60)
    
    try:
        # Create test documents
        test_files = create_test_documents()
        print(f"✅ Created {len(test_files)} test documents")
        
        # Initialize document store
        doc_store = DocumentStore(db_path="./test_chroma_db")
        print("✅ Initialized DocumentStore")
        
        # Load documents
        result = doc_store.load_documents(test_files)
        print(f"✅ Loaded documents: {result['processed_files']} files, {result['total_chunks']} chunks")
        
        # Check collection count
        count = doc_store.get_collection_count()
        print(f"✅ ChromaDB contains {count} chunks")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False

def test_question_answering():
    """Test question answering pipeline."""
    print("\n" + "="*60)
    print("TEST 2: Question Answering")
    print("="*60)
    
    try:
        # Initialize QA engine
        qa_engine = QAEngine(db_path="./test_chroma_db")
        print("✅ Initialized QA Engine")
        
        # Test questions
        test_questions = [
            "Who created Python?",
            "When was Python first released?",
            "What are the key features of Python?",
            "What is a dictionary in Python?",
            "What is Java?" # This should return "Answer not found"
        ]
        
        print("\nAsking test questions:\n")
        
        for i, question in enumerate(test_questions, 1):
            print(f"\nQuestion {i}: {question}")
            print("-" * 60)
            
            result = qa_engine.answer_question(question)
            
            print(f"Answer: {result['answer'][:200]}...")
            if result['sources']:
                print(f"Sources: {', '.join(result['sources'])}")
            print()
        
        print("✅ Question answering test completed")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_context_retrieval():
    """Test context retrieval without LLM."""
    print("\n" + "="*60)
    print("TEST 3: Context Retrieval (No LLM)")
    print("="*60)
    
    try:
        qa_engine = QAEngine(db_path="./test_chroma_db")
        
        question = "What is Python?"
        contexts = qa_engine.retrieve_context(question, top_k=3)
        
        print(f"Question: {question}")
        print(f"Retrieved {len(contexts)} context chunks:\n")
        
        for i, ctx in enumerate(contexts, 1):
            print(f"Context {i}:")
            print(f"  Text: {ctx['text'][:150]}...")
            print(f"  Source: {ctx['source']}")
            if ctx['distance']:
                print(f"  Distance: {ctx['distance']:.4f}")
            print()
        
        print("✅ Context retrieval test completed")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False

def cleanup_test_data():
    """Clean up test database."""
    print("\n" + "="*60)
    print("Cleaning up test data...")
    print("="*60)
    
    try:
        import shutil
        if os.path.exists("./test_chroma_db"):
            shutil.rmtree("./test_chroma_db")
            print("✅ Test database removed")
    except Exception as e:
        print(f"⚠️  Could not remove test database: {str(e)}")

def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("EXAM QA SYSTEM - TEST SUITE")
    print("="*60)
    
    results = []
    
    # Run tests
    results.append(("Document Loading", test_document_loading()))
    results.append(("Context Retrieval", test_context_retrieval()))
    
    # Only test QA if GPT4All model is available
    print("\n⚠️  Note: Question Answering test requires GPT4All model")
    response = input("Do you want to test Question Answering? (y/n): ")
    if response.lower() == 'y':
        results.append(("Question Answering", test_question_answering()))
    
    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name:30} {status}")
    
    print("="*60)
    
    # Cleanup
    cleanup_response = input("\nDo you want to clean up test data? (y/n): ")
    if cleanup_response.lower() == 'y':
        cleanup_test_data()
    
    print("\n✅ Testing complete!")

if __name__ == "__main__":
    main()
