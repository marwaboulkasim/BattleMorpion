from openai_client import OpenAIClient
from dotenv import load_dotenv
import os

load_dotenv()
MODELS=os.getenv("MODELS")
MODELS=tuple(MODELS.split())
URL=os.getenv("OLLAMA_TCP")+"/api/generate"
client_AI = OpenAIClient()