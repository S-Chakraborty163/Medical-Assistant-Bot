# 🏥 Medical Assistant Bot - AI-Powered Medical Document Q&A System

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.129.0-green)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.54.0-red)](https://streamlit.io/)
[![LangChain](https://img.shields.io/badge/LangChain-1.2.10-orange)](https://www.langchain.com/)
[![Pinecone](https://img.shields.io/badge/Pinecone-VectorDB-purple)](https://www.pinecone.io/)
[![Groq](https://img.shields.io/badge/Groq-LLM-yellow)](https://groq.com/)
[![License](https://img.shields.io/badge/License-MIT-lightgrey)](LICENSE)

## 📋 Overview

**Medical Assistant Bot** is an intelligent RAG (Retrieval-Augmented Generation) system that allows users to upload medical PDF documents and ask questions about their content. The system processes the documents, stores them in a vector database, and provides accurate, context-aware answers using state-of-the-art LLMs.

### ✨ Key Features

- **📄 Multi-PDF Upload**: Upload multiple medical PDF documents simultaneously
- **🔍 Semantic Search**: Pinecone vector database for efficient similarity search
- **🤖 Advanced LLM Integration**: Powered by Groq's Llama 3.3 70B model
- **💬 Interactive Chat**: Streamlit-based chat interface with history
- **📊 Source Attribution**: Responses include references to source documents
- **⚡ Fast Processing**: Asynchronous API with FastAPI backend
- **🔐 Secure**: Environment-based configuration for API keys
- **📱 Responsive UI**: Clean, user-friendly Streamlit frontend

🏗️ Architecture Overview:

<img width="599" height="542" alt="Screenshot 2026-02-16 180227" src="https://github.com/user-attachments/assets/8eacab2e-50d1-431b-989c-f5b7a46fe8e2" />

📡 Data Flow:

<img width="3946" height="3402" alt="deepseek_mermaid_20260216_20a819" src="https://github.com/user-attachments/assets/7c7fa02b-6ff7-4136-a6f9-5bc446aff346" />


## 📂 Directory Details

| Directory/File | Description |
|---------------|-------------|
| **.devcontainer/** | Development container configuration for consistent environments |
| **client/** | Frontend application with components and utilities |
| ├── components/ | Reusable UI components |
| ├── utils/ | Client-side helper functions |
| └── app.py | Main client application entry point |
| **server/** | Backend API server |
| ├── middlewares/ | Request/response middleware functions |
| ├── modules/ | Business logic modules |
| ├── routes/ | API route definitions |
| ├── logger.py | Logging configuration |
| └── main.py | Server entry point |
| **utils/** | Shared utilities used across client and server |
| **config.py** | Centralized configuration settings |
| **main.py** | Main application entry point |
| **requirements.txt** | Python dependencies |
| **pyproject.toml** | Project metadata and build configuration |
| **uv.lock** | Lock file for UV package manager |
| **DIABETES.pdf** | Reference documentation |
| **.gitignore** | Git ignore rules |
| **.python-version** | Python version specification |
| **README.md** | Project documentation |   


### 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Backend**: FastAPI
- **LLM Framework**: LangChain, LangChain-Groq
- **Vector Database**: Pinecone
- **Embeddings**: Google Generative AI Embeddings (gemini-embedding-001)
- **PDF Processing**: PyPDF
- **Language Model**: Llama-3.3-70b-versatile (Groq)
- **Logging**: Custom logger with StreamHandler


### 🚀 Getting Started

#### Prerequisites

- Python 3.10+
- Groq API Key
- Pinecone API Key
- Google Generative AI API Key

#### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/medical-assistant-bot.git
   cd medical-assistant-bot
   ```
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Add your API keys to .env
   ```
4. **Run the backend server**
   ```bash
   cd server
   uvicorn main:app --reload --port 8000
   ```
5. **Run the frontend application**
   ```bash
   cd client
   streamlit run app.py
   ```


🔧 Configuration:
Create a .env file with the following variables:
GROQ_API_KEY=your_groq_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENV=your_pinecone_environment
GOOGLE_API_KEY=your_google_api_key
API_URL=http://localhost:8000

## 📡 API Endpoints:

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/upload_pdfs/` | Upload PDF documents to the system. |
| `POST` | `/ask/` | Submit a question based on the uploaded PDFs. |

## 📖 Usage Examples

### 1. Uploading PDFs
**Endpoint:** `POST /upload_pdfs/` 

**Payload:** `multipart/form-data`

```bash
curl -X POST "[http://127.0.0.1:8000/upload_pdfs/](http://127.0.0.1:8000/upload_pdfs/)" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "files=@document1.pdf" \
     -F "files=@document2.pdf"
```
### 2. Asking a Question

**Endpoint:** `POST /ask/`

**Payload:** `application/json`

The endpoint expects a `POST` request with a JSON payload:

```json
{
  "question": "What are the key findings in the financial report?"
}
```
