import os
from dotenv import load_dotenv

# Force load .env from project directory
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=dotenv_path)

# Firecrawl
FIRECRAWL_KEY = os.getenv("FIRECRAWL_KEY", "")
FIRECRAWL_BASE_URL = os.getenv("FIRECRAWL_BASE_URL", "")
FIRECRAWL_CONCURRENCY = int(os.getenv("FIRECRAWL_CONCURRENCY", "2"))

# OpenAI / Custom LLM
OPENAI_KEY = os.getenv("OPENAI_KEY", "")
OPENAI_ENDPOINT = os.getenv("OPENAI_ENDPOINT", "https://api.openai.com/v1")
CUSTOM_MODEL = os.getenv("CUSTOM_MODEL", "")
CONTEXT_SIZE = int(os.getenv("CONTEXT_SIZE", "128000"))

# Fireworks / DeepSeek
FIREWORKS_KEY = os.getenv("FIREWORKS_KEY", "")

# App Config
PORT = int(os.getenv("PORT", "3051"))

# Debugging
#print(f"Firecrawl Key: {FIRECRAWL_KEY}")
#print(f"OpenAI Key: {OPENAI_KEY}")
