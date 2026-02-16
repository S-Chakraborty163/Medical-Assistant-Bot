import streamlit as st
import os
import tempfile
from pathlib import Path
from pinecone import Pinecone, ServerlessSpec
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_pinecone import PineconeVectorStore

# 1. Setup API Keys
os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
PINECONE_API_KEY = st.secrets["PINECONE_API_KEY"]

# --- ADDED: SPEED OPTIMIZATION (CACHING) ---
@st.cache_resource
def get_medical_retriever():
    """Initializes and caches the Pinecone connection so it's instant after the first load."""
    embed_model = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
    vectorstore = PineconeVectorStore(index_name="medicalindex", embedding=embed_model)
    # k=3 retrieves the best 3 chunks, making the prompt smaller and faster
    return vectorstore.as_retriever(search_kwargs={"k": 3})

@st.cache_resource
def get_chat_model():
    """Caches the Gemini Flash model, which is much faster for chat than the Pro version."""
    return ChatGoogleGenerativeAI(model="gemini-1.5-flash", streaming=True)

# Initialize the cached tools
retriever = get_medical_retriever()
llm = get_chat_model()
# --------------------------------------------

# 2. Initialize Pinecone (Existing code)
pc = Pinecone(api_key=PINECONE_API_KEY)
index_name = "medicalindex"

# 3. UI Logic (Existing code)
st.title("🩺 Medical Assistant Bot")
uploaded_files = st.file_uploader("Upload Medical PDFs", type="pdf", accept_multiple_files=True)

if st.button("Process & Index Documents"):
    if uploaded_files:
        with st.spinner("Processing..."):
            embed_model = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
            for uploaded_file in uploaded_files:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_path = tmp_file.name
                
                loader = PyPDFLoader(tmp_path)
                docs = loader.load()
                splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
                chunks = splitter.split_documents(docs)
                
                PineconeVectorStore.from_documents(
                    chunks, 
                    embed_model, 
                    index_name=index_name
                )
                os.remove(tmp_path)
            st.success("Documents successfully indexed!")
            # Refresh retriever after indexing new docs
            st.rerun() 
    else:
        st.error("Please upload files first.")

# 4. Chat Interface (UPDATED FOR SPEED)
if prompt := st.chat_input("Ask a medical question..."):
    st.chat_message("user").markdown(prompt)
    
    with st.chat_message("assistant"):
        # --- ADDED: STREAMING LOGIC ---
        # 1. Fast Retrieval
        docs = retriever.invoke(prompt)
        context = "\n".join([d.page_content for d in docs])
        
        # 2. Stream Response (Typewriter effect)
        full_prompt = f"Context: {context}\n\nQuestion: {prompt}"
        
        # This writes the response word-by-word as it's generated
        st.write_stream(llm.stream(full_prompt))