from langchain_ollama.chat_models import ChatOllama
from dotenv import load_dotenv

load_dotenv()

# LLM_MODEL = "deepseek-r1:14b"
# LLM_MODEL = "qwen2.5:7b"
# LLM_MODEL = "qwen3:14b"
LLM_MODEL = "qwen3:30b"

# llm = OllamaLLM(model=LLM_MODEL, temperature=0)
# LLM = OpenAI(model="gpt-4o", temperature=0.9)
# LLM = ChatOllama(model=LLM_MODEL, temperature=0.9)
# LLM = ChatOllama(model=LLM_MODEL, temperature=0.9)

def getLLM(model=LLM_MODEL, temperature=0.9):
    return ChatOllama(model=model, temperature=temperature)