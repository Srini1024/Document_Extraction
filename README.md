# 📚 Document Q&A Assistant

A Streamlit-based application that allows you to upload documents and ask questions about them using AI. The app uses RAG (Retrieval-Augmented Generation) to provide accurate answers based on your documents.

## ✨ Features

- **Document Upload**: Support for PDF, TXT, and DOCX files
- **AI-Powered Q&A**: Ask natural language questions about your documents
- **Source Citations**: View the specific document chunks used to generate answers
- **Persistent Storage**: ChromaDB vector database for efficient retrieval
- **Customizable**: Adjust LLM parameters (model, temperature, retrieval count)
- **Chat History**: Keep track of your conversation

## 🚀 Quick Start

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
export OPENAI_API_KEY="your-api-key-here"
```

### 3. Run the Application

```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

## 📖 How to Use

1. **Enter API Key**: In the sidebar, enter your OpenAI API key
2. **Configure Settings**: 
   - Choose your preferred LLM model (gpt-3.5-turbo, gpt-4, etc.)
   - Adjust temperature for response creativity
   - Set number of document chunks to retrieve
3. **Upload Documents**: Click "Browse files" and select your documents (PDF, TXT, or DOCX)
4. **Process Documents**: Click "Process Documents" to index your files
5. **Ask Questions**: Type your questions in the chat input at the bottom
6. **View Sources**: Expand the "View Sources" section to see which document chunks were used

## 🏗️ Architecture

```
User Query
    ↓
Question Processing
    ↓
Vector Search (ChromaDB) → Retrieve Relevant Chunks
    ↓
LLM Generation (OpenAI) → Generate Answer + Sources
    ↓
Display Response
```

## 📁 Project Structure

```
document_extraction_sample/
├── app.py                  # Main Streamlit application
├── extraction.py           # Original extraction script
├── requirements.txt        # Python dependencies
├── uploads/               # Uploaded documents storage
└── chroma_db/            # Vector database storage
```

## ⚙️ Configuration

### Default Settings

- **Chunk Size**: 500 characters
- **Chunk Overlap**: 50 characters
- **Embedding Model**: all-MiniLM-L6-v2 (HuggingFace)
- **Default LLM**: gpt-3.5-turbo
- **Default Temperature**: 0.7
- **Default Retrieval**: 3 documents

You can modify these in the sidebar or in the `app.py` file.

## 🔧 Advanced Usage

### Using Existing Vector Database

If you already have a `chroma_db` directory from running `extraction.py`, the app will automatically load it on startup.

### Processing Documents Programmatically

You can still use the original `extraction.py` script to process documents in batch:

```bash
python extraction.py
```

## 🛠️ Troubleshooting

### "No documents found"
- Make sure you've uploaded and processed documents using the sidebar
- Check that the `uploads/` directory contains your files

### "Error loading vector store"
- Delete the `chroma_db/` directory and reprocess your documents
- Ensure you have write permissions in the project directory

### "OpenAI API Error"
- Verify your API key is correct
- Check your OpenAI account has sufficient credits
- Ensure you have internet connectivity

## 📝 Example Questions

- "What is the main topic of this document?"
- "Summarize the key points about [specific topic]"
- "What does the document say about [specific question]?"
- "Find information related to [keyword]"

## 🔐 Security Notes

- Never commit your API keys to version control
- The API key entered in the sidebar is only stored in the session
- Consider using environment variables for production deployments

## 🤝 Contributing

Feel free to enhance this application by:
- Adding support for more document types
- Implementing different LLM providers (Anthropic, Cohere, etc.)
- Adding document management features
- Improving the UI/UX

## 📄 License

This is a sample project for educational purposes.


