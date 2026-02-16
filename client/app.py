import streamlit as st
import os
import tempfile
from pathlib import Path
from pinecone import Pinecone, ServerlessSpec
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
# Use the official Pinecone SDK for client initialization
from pinecone import Pinecone, ServerlessSpec 

# Use the specific LangChain-Pinecone integration package
from langchain_pinecone import PineconeVectorStore

# 1. Setup API Keys (Streamlit will get these from "Secrets")
os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
PINECONE_API_KEY = st.secrets["PINECONE_API_KEY"]

# 2. Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)
INDEX_NAME = "my-3072-dim-index"

# 3. UI Logic
st.title("🩺 Medical Assistant Bot")

uploaded_files = st.file_uploader("Upload Medical PDFs", type="pdf", accept_multiple_files=True)

if st.button("Process & Index Documents"):
    if uploaded_files:
        with st.spinner("Processing..."):
            embed_model = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
            
            for uploaded_file in uploaded_files:
                # Streamlit files are in memory; we must save them to a temp file for PyPDFLoader
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_path = tmp_file.name
                
                # Load and Split
                loader = PyPDFLoader(tmp_path)
                docs = loader.load()
                splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
                chunks = splitter.split_documents(docs)
                
                # Upsert to Pinecone
                # (Using the higher-level LangChain wrapper makes this much easier than manual zipping)
                PineconeVectorStore.from_documents(
                    chunks, 
                    embed_model, 
                    index_name=index_name
                )
                os.remove(tmp_path) # Clean up temp file
            st.success("Documents successfully indexed!")
    else:
        st.error("Please upload files first.")

# 4. Chat Interface
if prompt := st.chat_input("Ask a medical question..."):
    st.chat_message("user").markdown(prompt)
    st.chat_message("assistant").markdown("I'm processing your request based on the indexed docs...")

