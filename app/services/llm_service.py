import json
from app.helpers.StringHelper import normalize_messages
from app.libs.llm.ChatGPT import generate_chat
from app.libs.llm.Gemini import stream_chat
from app.libs.llm.Groq import groq_complete,stream_groq
from app.config import ACTIVE


def start():
    return ""

def chat(msg:str):
    if ACTIVE == "GEMINI":
        json_object = json.loads(msg)
        return generate_chat(normalize_messages(json_object))
    elif ACTIVE == "OPENAI":
        json_object = json.loads(msg)
        return stream_chat(normalize_messages(json_object))
    elif ACTIVE == "GROQ":
        json_object = json.loads(msg)
        return stream_groq(normalize_messages(json_object))

