# app/llm_groq.py
import os
import json
import time
from groq import Groq
from app.config import GROQ_API_KEY_2

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

SYSTEM_PROMPT = """
Kamu adalah chatbot AI general purpose.
Jawab dengan bahasa yang jelas, sopan, dan ringkas.
Sesuaikan bahasa dengan yang diinput user. Kalau bahasa indonesia jawab dengan bahasa indonesia, juga hal yang sama untuk bahasa lain

ATURAN WAJIB PENULISAN MATEMATIKA:
- Untuk formula inline gunakan \\( dan \\)
- Untuk formula blok gunakan \\[ dan \\]
- DILARANG menggunakan $ atau $$ sebagai delimiter matematika
- DILARANG menulis formula tanpa delimiter
- Contoh BENAR inline: \\(x^2 + y^2 = r^2\\)
- Contoh BENAR blok:
  \\[
  \\int_a^b f(x)\\,dx = F(b) - F(a)
  \\]
- Untuk numbered list rumus gunakan format:
  1. **Nama rumus**
     \\[formula\\]

ATURAN MATA UANG:
- DILARANG menggunakan simbol $ untuk mata uang
- Gunakan: USD, dolar, atau Rp untuk mata uang
"""

MODEL_NAME = "llama-3.3-70b-versatile"

client = Groq(api_key=GROQ_API_KEY_2)

def groq_complete(messages):
    """
    Pemanggilan Groq LLM sederhana
    messages = List[Message] atau raw JSON
    """

    msgs = messages

    # Konversi ke format API Groq
    body = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": msgs[0].role, "content": msgs[0].content}
    ]

    response = client.chat.completions.create(
        model=MODEL_NAME,  # model Groq API compatible
        messages=body
    )
    return response.choices[0].message.content.strip()


def stream_groq(messages):
    msgs = messages

    body = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": msgs[0].role, "content": msgs[0].content}
    ]

    stream = client.chat.completions.create(
        model=MODEL_NAME,
        messages=body,
        stream=True
    )

    #arr_chunk = []
    for chunk in stream:
        # chunk.choices[0].delta.content akan berisi token baru
        token = chunk.choices[0].delta.content
        if token:
            yield token
            #yield token.replace("| \n\n", "| \n\n\n")
            time.sleep(0.05)
            #arr_chunk.append(token.strip())
    yield "\n"
    yield "[DONE]"

def stream_with_table_detection(stream):
    table_buffer = []
    in_table = False

    for chunk in stream:
        if not chunk.choices:
            continue

        delta = chunk.choices[0].delta
        token = delta.content

        if not token:
            continue

        lines = token.splitlines(keepends=True)

        for line in lines:
            stripped = line.lstrip()

            # ── DETEKSI BARIS TABEL ─────────────────────
            if stripped.startswith("|"):
                in_table = True
                table_buffer.append(line)
                continue

            # ── KELUAR DARI TABEL ──────────────────────
            if in_table:
                # flush tabel sekaligus
                yield "".join(table_buffer).rstrip() + "\n\n"
                table_buffer.clear()
                in_table = False

            # ── STREAM NORMAL ──────────────────────────
            yield line
            time.sleep(0.05)

    # ── JIKA STREAM SELESAI SAAT MASIH DALAM TABEL ──
    if table_buffer:
        yield "".join(table_buffer).rstrip() + "\n\n"

