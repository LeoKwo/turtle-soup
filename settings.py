from langchain_ollama.chat_models import ChatOllama
from dotenv import load_dotenv
from langchain_ollama.embeddings import OllamaEmbeddings

load_dotenv()

LLM_MODEL = "qwen3:30b"
def getLLM(model=LLM_MODEL, temperature=0.9):
    return ChatOllama(model=model, temperature=temperature)

EMBED_MODEL = "herald/dmeta-embedding-zh"
def getEMBED(model=EMBED_MODEL):
    return OllamaEmbeddings(model=EMBED_MODEL)