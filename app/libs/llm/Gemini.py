# app/libs/llm/Gemini.py
import os
import time
from typing import Generator
from google import genai
from google.genai import types
import logging

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

GEMINI_MODELS = [
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-2.5-pro",
]

RATE_LIMIT_ERRORS = [
    "429",
    "quota",
    "exhausted",
    "rate_limit",
    "RESOURCE_EXHAUSTED",
    "too many requests",
    "exceeded your current quota",  
    "GenerateRequestsPerDay",        
    "free_tier",                     
    "retry",                         
]

def is_rate_limit_error(error_msg: str) -> bool:
    return any(x.lower() in error_msg.lower() for x in RATE_LIMIT_ERRORS)


def build_history(messages) -> list:
    """Konversi history messages ke format Gemini"""
    history = []
    for msg in messages[:-1]:
        history.append(
            types.Content(
                role="user" if msg.role == "user" else "model",
                parts=[types.Part(text=msg.content)]
            )
        )
    return history


def stream_gemini(messages, system_prompt: str) -> Generator[str, None, None]:
    history = build_history(messages)
    user_content = messages[-1].content

    for model in GEMINI_MODELS:
        try:
            print(f"Trying Gemini model: {model}")

            config = types.GenerateContentConfig(
                system_instruction=system_prompt,
            )

            # Gabungkan history + pesan baru
            contents = history + [
                types.Content(
                    role="user",
                    parts=[types.Part(text=user_content)]
                )
            ]

            response = client.models.generate_content_stream(
                model=model,
                contents=contents,
                config=config,
            )

            for chunk in response:
                if chunk.text:
                    yield chunk.text
                    time.sleep(0.5)

            yield "\n"
            yield "[DONE]"
            return

        except Exception as e:
            error_msg = str(e)
            logging.info(f"Gemini {model} error: {error_msg}")
            if is_rate_limit_error(error_msg):
                logging.info(f"Rate limit detected, trying next model...")
                continue
            else:
                logging.info(f"Non-rate-limit error, raising...")
                raise e

    logging.info("All Gemini models exhausted, raising to trigger Groq fallback...")
    raise Exception("All Gemini models rate limited or unavailable")


def complete_gemini(messages, system_prompt: str) -> str:
    history = build_history(messages)
    user_content = messages[-1].content

    for model in GEMINI_MODELS:
        try:
            config = types.GenerateContentConfig(
                system_instruction=system_prompt,
            )

            contents = history + [
                types.Content(
                    role="user",
                    parts=[types.Part(text=user_content)]
                )
            ]

            response = client.models.generate_content(
                model=model,
                contents=contents,
                config=config,
            )
            return response.text.strip()

        except Exception as e:
            error_msg = str(e)
            print(f"Gemini {model} error: {error_msg}")
            if is_rate_limit_error(error_msg):
                continue
            else:
                raise e

    raise Exception("All Gemini models rate limited or unavailable")