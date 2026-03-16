import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_KEY_2 = os.getenv("QROQ_API_KEY_2")
GROQ_API_KEY_3 = os.getenv("QROQ_API_KEY_3")
ACTIVE = os.getenv("ACTIVE")
