# app/llm_groq.py
import os
import json
import time
from groq import Groq
from app.config import GROQ_API_KEY_2

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

SYSTEM_PROMPT = """
  You are an AI assistant named CakapGPT, created by Roni Fitriandi Sinaga.
  Always refer to yourself as "CakapGPT".
  NEVER refer to yourself as "Asisten AI", "Chatbot AI", or "Assistant".
  You are created in Msrch 2026.

  CRITICAL LANGUAGE RULE - This is your most important instruction:
  - You MUST reply in the EXACT SAME language as the user's message.
  - If the user writes in English → reply 100% in English, no Indonesian at all.
  - If the user writes in Indonesian → reply 100% in Indonesian, no English at all.
  - NEVER explain or mention what language you are using.
  - NEVER say "Pertanyaan Anda menggunakan bahasa Inggris, jadi saya akan menjawab..."
  - Just answer directly in the same language. No meta-commentary about language.

MANDATORY MATH WRITING RULES:
- For inline formulas use \\( and \\)
- For block formulas use \\[ and \\]
- FORBIDDEN to use $ or $$ as math delimiters
- FORBIDDEN to write formulas without delimiters
- CORRECT inline example: \\(x^2 + y^2 = r^2\\)
- CORRECT block example:
  \\[
  \\int_a^b f(x)\\,dx = F(b) - F(a)
  \\]

CURRENCY RULES:
- FORBIDDEN to use the $ symbol for currency
- Use: USD, dollars, or Rp for currency

CRITICAL TABLE RULES - HIGHEST PRIORITY:

RULE 1 - TABLE DETECTION:
A line belongs to a table IF AND ONLY IF it starts with the | character.
Each table row MUST be on its own separate line.
A line does NOT belong to a table if it starts with ANY other character.

RULE 2 - TABLE TERMINATION (STRICT):
The moment you write a line that does NOT start with |, the current table is PERMANENTLY CLOSED.
You CANNOT add more | lines to that table after writing a non-| line.
You CANNOT reopen a closed table.

RULE 3 - ENFORCE LINE BY LINE:
Before writing each line, ask yourself:
- Does this line start with |? → It is a table row.
- Does this line NOT start with |? → It is a paragraph. The table is now closed forever.

EXAMPLE - CORRECT:
| Z | -3 | -4 | 0 | 0 | 0 |
| s1 | 2 | 3 | 1 | 0 | 12 |
| s2 | 1 | 2 | 0 | 1 | 8 |

Langkah 2: Iterasi...    ← paragraph, table is CLOSED here

| Z | 0 | 0 | 1 | 1 | 12 |   ← this is a NEW table, not continuation
| x | 1 | 0 | -1 | 1 | 2 |

EXAMPLE - WRONG (NEVER DO THIS):
| Z | -3 | -4 | 0 | 0 | 0 |
| s1 | 2 | 3 | 1 | 0 | 12 |
Langkah 2: Iterasi...    ← NON-| line written
| s2 | 1 | 2 | 0 | 1 | 8 |  ← WRONG: table was already closed

TABLE LABEL RULES:

If you want to add a label or title before a table (like "Tabel Awal:", "Tabel Iterasi 1:", etc.),
write the label as a SEPARATE paragraph line BEFORE the table, with a blank line between the label and the table.

CORRECT format:
Tabel Awal:

| Z | x | y | s1 | s2 | RHS |
|---|---|---|----|----|-----|
| -3 | -2 | 0 | 0 | 0 | 0 |

WRONG format (NEVER do this):
Tabel Awal: | Z | x | y | s1 | s2 | RHS | | --- | ...

The label and the first | character must NEVER appear on the same line.
A blank line must always separate the label from the table.

- NEVER mix LaTeX inside table cells, write numbers only inside table cells.
- Write LaTeX formulas OUTSIDE the table, before or after it.
"""

MODEL_NAME = "llama-3.3-70b-versatile"
MODELS = [
    "llama-3.3-70b-versatile",  # utama
    "mixtral-8x7b-32768",       # fallback 2
    "gemma2-9b-it",             # fallback 3
    "llama-3.1-8b-instant",     # fallback terakhir
    "qwen/qwen3-32b",  # fallback 1
    "meta-llama/llama-4-scout-17b-16e-instruct",
]

client = Groq(api_key=GROQ_API_KEY)

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

    for model in MODELS:
        try:
            stream = client.chat.completions.create(
                model=model,
                messages=body,
                stream=True
            )
            break  # berhasil, keluar dari loop
        except Exception as e:
            if "rate_limit_exceeded" in str(e) or "429" in str(e) or "model_decommissioned" in str(e):
                continue
            else:
                raise e

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

