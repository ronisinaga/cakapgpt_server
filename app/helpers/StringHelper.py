import re
import json
from typing import Any, List
from app.schemas.llm_schema import Message

def removeSpace(text):
    return re.sub(r'\s+', ' ', text)

def replaceUnicodeMinus(text:str)->str:
    replacements = {
        "−": "-",  # unicode minus
        "–": "-",  # en-dash (kadang muncul dari copy PDF)
        "—": "-",  # em-dash
        "×": "*",  # multiply symbol
        "·": "*",  # dot multiplication
        "÷": "/",  # division symbol
        "⁺": "+",  # superscript plus
        "⁻": "-",  # superscript minus
        "⁽": "(",  # unicode parenthesis
        "⁾": ")",
        " " : ""   # remove whitespace inside coefficients (optional)
    }
    for old, new in replacements.items():
        text = text.replace(old, new)

    return text.strip()

def normalize_messages(raw: Any) -> List[Message]:
    """
    Normalize input into List[Message]

    Accepts:
    - List[Message]
    - List[dict]
    - dict with key 'messages'
    - JSON string

    Returns:
    - List[Message]

    Raises:
    - TypeError / ValueError with clear message
    """

    # 1️⃣ JSON string → dict
    if isinstance(raw, str):
        try:
            raw = json.loads(raw)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON string for messages")

    # 2️⃣ dict → ambil messages
    if isinstance(raw, dict):
        if "messages" not in raw:
            raise KeyError("Missing 'messages' key in dict")
        raw = raw["messages"]

    # 3️⃣ HARUS list
    if not isinstance(raw, list):
        raise TypeError(f"Expected list of messages, got {type(raw)}")

    normalized: List[Message] = []

    for i, msg in enumerate(raw):
        # 4️⃣ Sudah Message
        if isinstance(msg, Message):
            normalized.append(msg)

        # 5️⃣ dict → Message
        elif isinstance(msg, dict):
            if "role" not in msg or "content" not in msg:
                raise ValueError(
                    f"Message at index {i} must have 'role' and 'content'"
                )
            normalized.append(Message(**msg))

        else:
            raise TypeError(
                f"Invalid message type at index {i}: {type(msg)}"
            )

    return normalized
