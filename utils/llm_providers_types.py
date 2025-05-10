from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq

LLM_PROVIDERS_TYPES = {
    'OpenAI': {
        'models': ['gpt-4.1-nano','gpt-4o-mini'],
        'llm_model': ChatOpenAI
    },
    'Groq': {
        'models': ['gemma2-9b-it','llama-3.3-70b-versatile','llama-3.1-8b-instant','llama-guard-3-8b','llama3-8b-8192'],
        'llm_model': ChatGroq
    },
}