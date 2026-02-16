import streamlit as st
import os
import tempfile
from pinecone import Pinecone
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_pinecone import PineconeVectorStore

# 1. Setup API Keys & Constants
os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
PINECONE_API_KEY = st.secrets["PINECONE_API_KEY"]
# Use your specific index name here
INDEX_NAME = "my-3072-dim-index"

# 2. Optimized Resource Loading
@st.cache_resource
def get_resources():
    # gemini-embedding-001 outputs 3072 dimensions by default
    embed_model = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
    
    # Initialize VectorStore with your specific index
    vectorstore = PineconeVectorStore(index_name=INDEX_NAME, embedding=embed_model)
    
    # Initialize fast chat model
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", streaming=True)
    
    return vectorstore.as_retriever(search_kwargs={"k": 3}), llm

retriever, llm = get_resources()

# 3. UI Logic
st.title("🩺 Medical Assistant Bot")
uploaded_files = st.file_uploader("Upload Medical PDFs", type="pdf", accept_multiple_files=True)

if st.button("Process & Index Documents"):
    if uploaded_files:
        with st.spinner("Processing into 3072-dimensional space..."):
            embed_model = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
            for uploaded_file in uploaded_files:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(uploaded_file.getvalue())
                    loader = PyPDFLoader(tmp.name)
                    docs = loader.load()
                    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=80)
                    chunks = splitter.split_documents(docs)
                    
                    # Ensure we are uploading to the correct 3072-dim index
                    PineconeVectorStore.from_documents(
                        chunks, embed_model, index_name=INDEX_NAME
                    )
                    os.remove(tmp.name)
            st.success("Indexing Complete!")
            st.rerun()

# 4. Fast Chat Interface
if prompt := st.chat_input("Ask a medical question..."):
    st.chat_message("user").markdown(prompt)
    
    with st.chat_message("assistant"):
        # Retrieve context from your high-dim index
        docs = retriever.invoke(prompt)
        context = "\n\n".join([d.page_content for d in docs])
        
        # Stream the response
        full_prompt = f"Using this medical context: {context}\n\nAnswer the question: {prompt}"
        st.write_stream(llm.stream(full_prompt))