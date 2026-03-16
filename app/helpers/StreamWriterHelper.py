from fastapi import FastAPI, Response
import asyncio

async def StreamCharWriter(list_str:list):
    for str in list_str:
        #print(str)
        #StreamCharOfTextWriter(str)
        for word in str.split():
            for char in word:
                yield f"{char}"
                await asyncio.sleep(0.05)
            yield " "
        yield f" \n"
    #StreamDoneWriter("[DONE]")
    yield f"[DONE]"

async def StreamWordWriter(list_str:list):
    for str in list_str:
       #await StreamWordOfTextWriter(str)
        for word in str.split():
            yield f"{word} "
            await asyncio.sleep(0.2)
        yield f"\n\n"
    #StreamDoneWriter("[DONE]")
    yield f"[DONE]"

async def StreamTextWriter(list_str:list):
    for str in list_str:
       #await StreamWordOfTextWriter(str)
        yield f"{str} "
        await asyncio.sleep(0.2)
    yield f"\n"
    #StreamDoneWriter("[DONE]")
    yield f"[DONE]"

async def StreamCharOfTextWriter(text:str):
    for word in text.split():
        for char in word:
            yield f"{char}"
            await asyncio.sleep(0.05)
        yield " "
    yield f" \n"

async def StreamWordOfTextWriter(text:str):
    for word in str.split():
        yield f"{word}\n\n"
        await asyncio.sleep(0.05)
    yield f"\n"

async def StreamDoneWriter(text:str):
    yield "data: [DONE]"