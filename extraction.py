import os
import shutil
from langchain_community.document_loaders import PyPDFLoader, TextLoader , Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

UPLOAD_DIR = 'uploads' 
CHUNK_SIZE = 2000
CHUNK_OVERLAP = 400
VECTOR_DB_PATH = "./chroma_db" 
MODEL_NAME = "all-MiniLM-L6-v2"

def load_and_chunk_files(filepaths):
    """Load documents and split them into chunks."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        is_separator_regex=False,
    )

    all_chunks = []

    for filepath in filepaths:
        filename = os.path.basename(filepath)
        print(f"Processing file: {filename}...")
        try:
            if filename.lower().endswith('.pdf'):
                loader = PyPDFLoader(filepath)
            elif filename.lower().endswith('.txt'):
                loader = TextLoader(filepath)
            elif filename.lower().endswith('.docx'):
                loader = Docx2txtLoader(filepath)
            else:
                print(f"  -> Skipping unsupported file type: {filename}")
                continue

            documents = loader.load()

            if documents:
                chunks = text_splitter.split_documents(documents)
                all_chunks.extend(chunks)
                print(f"  -> Successfully split into {len(chunks)} chunks.")
            else:
                print(f"  -> No content loaded from file: {filename}")

        except Exception as e:
            print(f"  -> ERROR processing {filename}: {e}")
            
    return all_chunks

def text_extraction_and_chunking():
    print(f"Starting document processing in directory: {UPLOAD_DIR}\n")
    
    filepaths = []
    if os.path.exists(UPLOAD_DIR):
        for filename in os.listdir(UPLOAD_DIR):
            filepath = os.path.join(UPLOAD_DIR, filename)
            if os.path.isfile(filepath):
                filepaths.append(filepath)

    all_chunks = load_and_chunk_files(filepaths)
    
    print("\n--- Processing Complete ---")
    print(f"Total documents processed: {len(filepaths)} files checked.")
    print(f"Total chunks created across all documents: {len(all_chunks)}")
    
    return all_chunks

def get_vectorstore(chunks):
    """Embeds the chunks and indexes them in Chroma."""

    if os.path.exists(VECTOR_DB_PATH):
        print(f"Removing old database at: {VECTOR_DB_PATH}")
        shutil.rmtree(VECTOR_DB_PATH)
    
    print(f"Initializing embedding model: {MODEL_NAME}...")
    embeddings = HuggingFaceEmbeddings(model_name=MODEL_NAME)

    print(f"Creating new Chroma DB at: {VECTOR_DB_PATH}")
    
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=VECTOR_DB_PATH
    )
    vectorstore.persist()
    print("✅ New database created successfully!")
    return vectorstore

def load_vectorstore():
    """Loads the existing vectorstore from disk."""
    try:
        embeddings = HuggingFaceEmbeddings(model_name=MODEL_NAME)
        vectorstore = Chroma(
            persist_directory=VECTOR_DB_PATH,
            embedding_function=embeddings
        )
        return vectorstore
    except Exception as e:
        print(f"Error loading vector store: {e}")
        return None

def index_and_retrieve_documents(chunks: list[Document]):
    """Embeds the chunks, indexes them in Chroma, and tests retrieval."""
    
    if not chunks:
        print("No chunks to process. Indexing skipped.")
        return
        
    print("\n" + "="*50)
    print("STEP 2: EMBEDDING AND INDEXING")
    print("="*50)
    
    vectorstore = get_vectorstore(chunks)
    
    print("\nPipeline execution complete.")


if __name__ == "__main__":
    all_document_chunks = text_extraction_and_chunking()
    
    index_and_retrieve_documents(all_document_chunks)