🩺 Medical Assistant Bot (RAG-Powered):

An intelligent, document-aware Medical Assistant built with LangChain, Pinecone, and Google Gemini. This application allows users to upload medical PDFs and ask complex health questions, receiving real-time, contextually accurate answers backed by their own data.

🚀 Features:
High-Speed RAG: Utilizes gemini and optimized caching for near-instant responses.

PDF Knowledge Base: Interactive file uploader that processes, chunks, and indexes documents on the fly.

3072-Dim Vector Search: Uses high-resolution embeddings (gemini-embedding-001) for superior semantic understanding.

Real-time Streaming: Answers are streamed word-by-word (typewriter effect) for a modern chat experience.

Cloud Optimized: Fully compatible with Streamlit Cloud secrets management and ephemeral server environments.


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

