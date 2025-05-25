from langchain_community.vectorstores.faiss import FAISS
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from settings import getEMBED

def search(query: str):
    embedding = getEMBED()
    vectorstore = FAISS.load_local("soup_index", embedding, allow_dangerous_deserialization=True)
    results = vectorstore.similarity_search(query, k=3)

    print(f"=== RAG RESULT: [{query}] ===")
    for res in results:
        print("content:", res.page_content)
        print("----")
    print("=== RAG RESULT ===\n")
    return results

if __name__ == "__main__":
    search("夜晚有人敲门但没人出现")
