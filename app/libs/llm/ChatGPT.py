from openai import OpenAI
from app.config import OPENAI_API_KEY

print(OPENAI_API_KEY)

client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """
Kamu adalah chatbot AI general purpose.
Jawab dengan bahasa yang jelas, sopan, dan ringkas.
Sesuaikan bahasa dengan yang diinput user. Kalau bahasa indonesia jawab dengan bahasa indonesia, juga hal yang sama untuk bahasa lain
"""

def generate_chat(messages):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            *messages
        ],
        temperature=0.7
    )
    return response.choices[0].message.content
