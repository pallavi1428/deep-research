from openai import OpenAI
import tiktoken
from config import (
    OPENAI_KEY,
    OPENAI_ENDPOINT,
    CUSTOM_MODEL,
    CONTEXT_SIZE,
)

class LanguageModel:
    def __init__(self, model_name: str = "gpt-4", base_url: str = OPENAI_ENDPOINT):
        self.client = OpenAI(api_key=OPENAI_KEY, base_url=base_url)
        self.model_name = model_name

    def generate(self, messages: list, max_tokens: int = 2048):
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=0.7,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content.strip()

# Model singleton
_model = None

def get_model() -> LanguageModel:
    global _model
    if _model is None:
        model_id = CUSTOM_MODEL if CUSTOM_MODEL else "gpt-4"
        _model = LanguageModel(model_name=model_id)
    return _model

# Tokenizer for trimming
ENCODER = tiktoken.encoding_for_model("gpt-4")
MIN_CHUNK_SIZE = 140

def trim_prompt(prompt: str, context_size: int = CONTEXT_SIZE) -> str:
    if not prompt:
        return ""
    encoded = ENCODER.encode(prompt)
    if len(encoded) <= context_size:
        return prompt

    overflow = len(encoded) - context_size
    est_chars = overflow * 3
    cut_length = max(len(prompt) - est_chars, MIN_CHUNK_SIZE)
    return prompt[:cut_length]
