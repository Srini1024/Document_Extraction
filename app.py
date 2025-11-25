import streamlit as st
import os
from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from extraction import load_and_chunk_files, get_vectorstore, load_vectorstore


load_dotenv()
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
except ImportError:
    ChatGoogleGenerativeAI = None
UPLOAD_DIR = 'uploads'

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'vectorstore' not in st.session_state:
    st.session_state.vectorstore = None
if 'qa_chain' not in st.session_state:
    st.session_state.qa_chain = None

st.set_page_config(
    page_title="Document Q&A Assistant",
    page_icon="📁",
    layout="wide"
)

def initialize_qa_chain(api_key, model_choice, temperature, k_docs, provider):
    """Initialize the QA chain with LLM."""
    if not st.session_state.vectorstore:
        st.session_state.vectorstore = load_vectorstore()
    
    if not st.session_state.vectorstore:
        return None
    
    try:
        if provider == "Google Gemini (Free Tier)":
            llm = ChatGoogleGenerativeAI(
                model=model_choice,
                google_api_key=api_key,
                temperature=temperature
            )

        else:
            st.error(f"Unknown provider: {provider}")
            return None
    except Exception as e:
        st.error(f"Error initializing LLM: {e}")
        return None
    
    prompt_template = """You are a helpful assistant that answers questions based on the provided documents.

    Use the following context from the documents to answer the question. 
    Always start your answer with phrases like "According to the documentation..." or "Based on the documents..." or "The documentation states..."
    If you don't know the answer or cannot find it in the context, say "I cannot find this information in the provided documents."
    
    Context from documents:
    {context}
    
    Question: {question}
    
    Answer (start with "According to the documentation..." or similar):"""
    
    PROMPT = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=st.session_state.vectorstore.as_retriever(search_kwargs={"k": k_docs}),
        chain_type_kwargs={"prompt": PROMPT},
        return_source_documents=True
    )
    
    return qa_chain

provider = "Google Gemini (Free Tier)" if ChatGoogleGenerativeAI else None
api_key = os.getenv("GOOGLE_API_KEY")
model_choice = "gemini-2.5-pro" 
temperature = 0.7 
k_docs = 3  

st.title("📚 Document Q&A Assistant")
st.markdown("Ask questions about the documents using AI")


if not st.session_state.vectorstore:
    if os.path.exists("./chroma_db"):
        with st.spinner("Loading documents..."):
            st.session_state.vectorstore = load_vectorstore()
        if st.session_state.vectorstore:
            st.success("✅ Documents loaded successfully!")
    else:
        st.error("⚠️ No documents found. Please contact the administrator to configure documents.")


if api_key and st.session_state.vectorstore and provider:
 
    if not st.session_state.qa_chain:
        st.session_state.qa_chain = initialize_qa_chain(api_key, model_choice, temperature, k_docs, provider)
    
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if prompt := st.chat_input("Ask a question about the documents"):

        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = st.session_state.qa_chain({"query": prompt})
                    answer = response["result"]
                    
                    st.markdown(answer)
                    
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": answer
                    })
                
                except Exception as e:
                    st.error(f"Error generating response: {e}")

elif not api_key or not provider:
    st.error("⚠️ System configuration error. Please contact the administrator.")


# st.divider()
