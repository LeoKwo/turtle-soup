import json
import requests
from langchain_core.documents import Document
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_community.vectorstores.faiss import FAISS
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from settings import getEMBED

embedding = getEMBED()

docs = []
with open("soup.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        data = json.loads(line)
        content = f"{data['soup']}\n\n故事真相:\n{data['story']}"
        metadata = {}
        docs.append(Document(page_content=content, metadata=metadata))

with open("soup2.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        data = json.loads(line)
        content = f"{data['soup']}\n\n故事真相:\n{data['story']}"
        metadata = {}
        docs.append(Document(page_content=content, metadata=metadata))

# Create vector store
vectorstore = FAISS.from_documents(docs, embedding)

# Save to disk
vectorstore.save_local("soup_index")
