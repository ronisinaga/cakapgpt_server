import google.generativeai as genai
from app.config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = """
Jawab dengan bahasa yang jelas, sopan, dan ringkas.
Sesuaikan bahasa dengan yang diinput user. Kalau bahasa indonesia jawab dengan bahasa indonesia, juga hal yang sama untuk bahasa lain
"""

model = genai.GenerativeModel(
    model_name="models/gemini-2.5-flash",
    system_instruction=SYSTEM_PROMPT
)

def convert_messages(messages):
    history = []
    for msg in messages:
        if msg.role == "user":
            history.append({
                "role": "user",
                "parts": [msg.content]
            })
        elif msg.role == "assistant":
            history.append({
                "role": "model",
                "parts": [msg.content]
            })
    return history


def stream_chat(messages):
    arr_chunk = []
    history = convert_messages(messages)

    chat = model.start_chat(history=history)

    response = chat.send_message(
        messages[-1].content,
        stream=True
    )

    for chunk in response:
        #if chunk.text:
        if hasattr(chunk, "text") and chunk.text:
            #print(chunk.text)
            #yield chunk.text
            arr_chunk.append(chunk.text)
    
    return arr_chunk