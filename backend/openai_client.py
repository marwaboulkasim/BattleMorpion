from openai import AzureOpenAI
from dotenv import load_dotenv
import os

class OpenAIClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            load_dotenv()
            cls._instance = AzureOpenAI(
                api_key=os.getenv("AZURE_API_KEY"),
                azure_endpoint=os.getenv("AZURE_ENDPOINT"),
                api_version=os.getenv("AZURE_API_VERSION"),
            )
        return cls._instance