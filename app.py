"""
PyQt5 GUI application for offline exam answer retrieval system.
Provides interface for document loading and question answering.
"""

import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QTextEdit, QLabel, 
                             QFileDialog, QMessageBox, QProgressBar, QTabWidget,
                             QListWidget, QSplitter)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont
from embed_store import DocumentStore
from qa_engine import QAEngine


class DocumentLoadThread(QThread):
    """Thread for loading documents without blocking UI."""
    progress = pyqtSignal(str)
    finished = pyqtSignal(dict)
    
    def __init__(self, doc_store, file_paths):
        super().__init__()
        self.doc_store = doc_store
        self.file_paths = file_paths
    
    def run(self):
        self.progress.emit("Loading documents...")
        result = self.doc_store.load_documents(self.file_paths)
        self.finished.emit(result)


class QAThread(QThread):
    """Thread for answering questions without blocking UI."""
    finished = pyqtSignal(dict)
    
    def __init__(self, qa_engine, question):
        super().__init__()
        self.qa_engine = qa_engine
        self.question = question
    
    def run(self):
        result = self.qa_engine.answer_question(self.question)
        self.finished.emit(result)


class ExamQAApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.doc_store = None
        self.qa_engine = None
        self.init_ui()
        self.init_engines()
    
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Offline Exam Answer Retrieval System")
        self.setGeometry(100, 100, 1000, 700)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Title
        title = QLabel("🎓 Secure Offline Exam System")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        
        # Tab widget
        tabs = QTabWidget()
        main_layout.addWidget(tabs)
        
        # Document Management Tab
        doc_tab = QWidget()
        doc_layout = QVBoxLayout(doc_tab)
        
        # Document loading section
        doc_label = QLabel("📚 Load Exam Documents (PDF, DOCX, TXT)")
        doc_label.setFont(QFont("Arial", 12))
        doc_layout.addWidget(doc_label)
        
        btn_layout = QHBoxLayout()
        self.btn_load_docs = QPushButton("Load Documents")
        self.btn_load_docs.clicked.connect(self.load_documents)
        btn_layout.addWidget(self.btn_load_docs)
        
        self.btn_clear_db = QPushButton("Clear Database")
        self.btn_clear_db.clicked.connect(self.clear_database)
        btn_layout.addWidget(self.btn_clear_db)
        
        doc_layout.addLayout(btn_layout)
        
        # Status display
        self.doc_status = QTextEdit()
        self.doc_status.setReadOnly(True)
        self.doc_status.setMaximumHeight(150)
        self.doc_status.setPlaceholderText("Document loading status will appear here...")
        doc_layout.addWidget(self.doc_status)
        
        # Loaded files list
        list_label = QLabel("Loaded Document Chunks:")
        doc_layout.addWidget(list_label)
        self.loaded_files_list = QListWidget()
        doc_layout.addWidget(self.loaded_files_list)
        
        tabs.addTab(doc_tab, "Document Management")
        
        # Q&A Tab
        qa_tab = QWidget()
        qa_layout = QVBoxLayout(qa_tab)
        
        # Question input
        q_label = QLabel("❓ Enter Your Question:")
        q_label.setFont(QFont("Arial", 12))
        qa_layout.addWidget(q_label)
        
        self.question_input = QTextEdit()
        self.question_input.setMaximumHeight(100)
        self.question_input.setPlaceholderText("Type your exam question here...")
        qa_layout.addWidget(self.question_input)
        
        # Ask button
        self.btn_ask = QPushButton("Get Answer")
        self.btn_ask.clicked.connect(self.ask_question)
        self.btn_ask.setEnabled(False)
        qa_layout.addWidget(self.btn_ask)
        
        # Answer display
        answer_label = QLabel("📝 Answer:")
        answer_label.setFont(QFont("Arial", 12))
        qa_layout.addWidget(answer_label)
        
        self.answer_display = QTextEdit()
        self.answer_display.setReadOnly(True)
        self.answer_display.setPlaceholderText("Answer will appear here...")
        qa_layout.addWidget(self.answer_display)
        
        # Sources display
        sources_label = QLabel("📄 Sources:")
        qa_layout.addWidget(sources_label)
        self.sources_display = QTextEdit()
        self.sources_display.setReadOnly(True)
        self.sources_display.setMaximumHeight(80)
        qa_layout.addWidget(self.sources_display)
        
        tabs.addTab(qa_tab, "Question & Answer")
        
        # Status bar
        self.statusBar().showMessage("Ready - Please load documents first")
    
    def init_engines(self):
        """Initialize document store and QA engine."""
        try:
            self.doc_store = DocumentStore()
            self.qa_engine = QAEngine()
            self.update_doc_count()
        except Exception as e:
            QMessageBox.critical(self, "Initialization Error", 
                               f"Failed to initialize engines:\n{str(e)}")
    
    def load_documents(self):
        """Open file dialog and load selected documents."""
        file_paths, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Exam Documents",
            "",
            "Documents (*.pdf *.docx *.txt);;All Files (*.*)"
        )
        
        if not file_paths:
            return
        
        self.btn_load_docs.setEnabled(False)
        self.doc_status.append(f"Selected {len(file_paths)} file(s)")
        
        # Start loading thread
        self.load_thread = DocumentLoadThread(self.doc_store, file_paths)
        self.load_thread.progress.connect(self.update_load_progress)
        self.load_thread.finished.connect(self.on_load_finished)
        self.load_thread.start()
    
    def update_load_progress(self, message):
        """Update progress message."""
        self.doc_status.append(message)
    
    def on_load_finished(self, result):
        """Handle document loading completion."""
        self.btn_load_docs.setEnabled(True)
        
        msg = f"\n✅ Loading Complete!\n"
        msg += f"Processed Files: {result['processed_files']}\n"
        msg += f"Total Chunks: {result['total_chunks']}"
        self.doc_status.append(msg)
        
        self.update_doc_count()
        self.btn_ask.setEnabled(True)
        self.statusBar().showMessage(f"Ready - {result['total_chunks']} chunks loaded")
        
        QMessageBox.information(self, "Success", 
                              f"Successfully loaded {result['processed_files']} document(s)")
    
    def clear_database(self):
        """Clear all documents from database."""
        reply = QMessageBox.question(self, "Confirm Clear",
                                    "Are you sure you want to clear all documents?",
                                    QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.doc_store.clear_database()
            self.doc_status.append("\n🗑️ Database cleared")
            self.update_doc_count()
            self.btn_ask.setEnabled(False)
            self.statusBar().showMessage("Database cleared - Please load documents")
    
    def update_doc_count(self):
        """Update the document count display."""
        count = self.doc_store.get_collection_count()
        self.loaded_files_list.clear()
        self.loaded_files_list.addItem(f"Total chunks in database: {count}")
    
    def ask_question(self):
        """Process user question."""
        question = self.question_input.toPlainText().strip()
        
        if not question:
            QMessageBox.warning(self, "Empty Question", "Please enter a question")
            return
        
        self.btn_ask.setEnabled(False)
        self.answer_display.setText("🔍 Searching documents and generating answer...")
        self.sources_display.clear()
        
        # Start QA thread
        self.qa_thread = QAThread(self.qa_engine, question)
        self.qa_thread.finished.connect(self.on_answer_ready)
        self.qa_thread.start()
    
    def on_answer_ready(self, result):
        """Display the generated answer."""
        self.btn_ask.setEnabled(True)
        
        # Display answer
        self.answer_display.setText(result['answer'])
        
        # Display sources
        if result['sources']:
            sources_text = "Sources: " + ", ".join(result['sources'])
            self.sources_display.setText(sources_text)
        else:
            self.sources_display.setText("No sources found")
        
        self.statusBar().showMessage("Answer generated")


def main():
    """Main application entry point."""
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    window = ExamQAApp()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
