# from backend.openai_client import OpenAIClient
from dotenv import load_dotenv
import os

load_dotenv()
MODELS=tuple(os.getenv("MODELS", "").replace(",", " ").split())
URL=os.getenv("OLLAMA_TCP")
# client_AI = OpenAIClient()

print(MODELS)
print(MODELS[0])
print(MODELS[1])