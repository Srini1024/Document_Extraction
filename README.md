#  Document Q&A Assistant

A Streamlit-based application that allows you to upload documents and ask questions about them using AI. The app uses RAG (Retrieval-Augmented Generation) to provide accurate answers based on your documents.
For testing purposes I have used one example document which you can view in the uploads folder. 
## Features

- **Document Upload**: Support for PDF, TXT, and DOCX files
- **AI-Powered Q&A**: Ask natural language questions about your documents
- **Persistent Storage**: ChromaDB vector database for efficient retrieval
- **Customizable**: Adjust LLM parameters (model, temperature, retrieval count)
- **Chat History**: Keep track of your conversation

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up OpenAI API Key

You have two options:

**Option A: Enter in the app (Recommended for testing)**
- Run the app and enter your API key in the sidebar

**Option B: Use environment variable**
```bash
export GOOGLE_API_KEY="your-api-key-here"
```

### 3. Run the Application

```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`


## Architecture

```
User Query
    ↓
Question Processing
    ↓
Vector Search (ChromaDB) → Retrieve Relevant Chunks
    ↓
LLM Generation (GEMINI) → Generate Answer using relevant chunks
    ↓
Display Response
```

## Project Structure

```
document_extraction_sample/
├── app.py                  # Main Streamlit application
├── extraction.py           # Original extraction script
├── requirements.txt        # Python dependencies
├── uploads/               # Uploaded documents storage
└── chroma_db/            # Vector database storage
```

## Configuration

### Default Settings

- **Chunk Size**: 2000 characters
- **Chunk Overlap**: 400 characters
- **Embedding Model**: all-MiniLM-L6-v2 (HuggingFace)
- **Default LLM**: gemini-2.5-pro
- **Default Temperature**: 0.7
- **Default Retrieval**: 3 documents

You can modify these in the extraction.py and app.py code according to your requirements.


### Using Existing Vector Database

If you already have a `chroma_db` directory from running `extraction.py`, the app will automatically load it on startup.

### Processing Documents Programmatically

You can still use the original `extraction.py` script to process documents in batch:

```bash
python extraction.py
```

## License

This is a sample project for educational purposes.


