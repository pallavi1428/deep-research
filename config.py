import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

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
