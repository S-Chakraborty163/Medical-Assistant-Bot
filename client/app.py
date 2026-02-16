import streamlit as st
from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI

# 1. CACHE THE HEAVY STUFF (Models and DB Connections)
@st.cache_resource
def get_retriever():
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    # Connecting to the cloud index once, then reusing it
    vectorstore = PineconeVectorStore(index_name="medicalindex", embedding=embeddings)
    return vectorstore.as_retriever(search_kwargs={"k": 3}) # Retrieve fewer, high-quality chunks

@st.cache_resource
def get_llm():
    return ChatGoogleGenerativeAI(model="gemini-1.5-flash", streaming=True)

# Initialize
retriever = get_retriever()
llm = get_llm()

# 2. THE CHAT INTERFACE
if prompt := st.chat_input("Ask a medical question..."):
    st.chat_message("user").markdown(prompt)
    
    with st.chat_message("assistant"):
        # Retrieve context fast
        docs = retriever.invoke(prompt)
        context = "\n".join([d.page_content for d in docs])
        
        # Stream the response like a typewriter
        # This is where the "speed" comes from
        full_prompt = f"Context: {context}\n\nQuestion: {prompt}"
        response_generator = llm.stream(full_prompt)
        st.write_stream(response_generator)