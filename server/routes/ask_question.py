from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse
from modules.llm import get_llm_chain
from modules.query_handlers import query_chain
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from pinecone import Pinecone, ServerlessSpec
from pydantic import Field
from typing import List, Optional
from logger import logger
import os

router=APIRouter()

@router.post("/ask/")
async def ask_question(question: str = Form(...)):
    try:
        logger.info(f"user query: {question}")

        # Embed model + Pinecone setup
        pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
        index_name = "my-3072-dim-index"
        if index_name not in pc.list_indexes().names():
             pc.create_index(
                  name=index_name,
                  dimension=3072,  # Match your embedding dimension
                  metric="cosine",  # or "euclidean" depending on your needs
                  spec=ServerlessSpec(cloud="aws",region = os.environ.get("PINECONE_ENV", "us-east-1"))
                  )
        print(f"Created new index: {index_name}")
        index = pc.Index(index_name)
        embed_model = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
        embedded_query = embed_model.embed_query(question)
        res = index.query(vector=embedded_query, top_k=3, include_metadata=True)

        docs = [
            Document(
                page_content=match["metadata"].get("text", ""),
                metadata=match["metadata"]
            ) for match in res["matches"]
        ]

        class SimpleRetriever(BaseRetriever):
            tags: Optional[List[str]] = Field(default_factory=list)
            metadata: Optional[dict] = Field(default_factory=dict)

            def __init__(self, documents: List[Document]):
                super().__init__()
                self._docs = documents

            def _get_relevant_documents(self, query: str) -> List[Document]:
                return self._docs

        retriever = SimpleRetriever(docs)
        chain = get_llm_chain(retriever)
        result = query_chain(chain, question)

        logger.info("query successful")
        return result

    except Exception as e:
        logger.exception("Error processing question")
        return JSONResponse(status_code=500, content={"error": str(e)})

