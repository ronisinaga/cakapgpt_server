import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from sse_starlette import EventSourceResponse
from app.routers.llm_router import llm_router
from app.routers.linear_router import linear_router
from app.routers.chat_router import chat_router
from app.routers.optimization_router import optimization_router
from app.routers.experiment_router import experiment_router
from app.helpers.StreamWriterHelper import StreamCharWriter
from fastapi.middleware.cors import CORSMiddleware
from app.controllers.chat_controller import welcome
import logging

app = FastAPI(title="Web API OKAPP")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://cakapgpt.com",
        "https://www.cakapgpt.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def read_root():
    return {"message": "Web API OKAPP Punya Roni Sinaga!"}

app.include_router(linear_router,prefix="/api/v1",tags=["Linear Equation"])
app.include_router(chat_router,prefix="/api/v1",tags=["Welcome message"])
app.include_router(optimization_router,prefix="/api/v1",tags=["Optimization"])
app.include_router(experiment_router,prefix="/api/v1",tags=["Optimization"])
app.include_router(llm_router,prefix="/api/v1",tags=["LLM"])

@app.get("/text")
async def sse_endpoint():
    arr = [
        "Tulisa pertama yang cukup panjang semoga bisa terlihat",
        "Tulisan kedua yang juga mirip tulisan pertama semoga bisa terlihat"
    ]
    return StreamingResponse(
        StreamCharWriter(arr), 
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*"
        }
    )

@app.get("/stream") 
async def stream(request: Request): 
    arr = [
        "Tulisa pertama yang cukup panjang semoga bisa terlihat",
        "Tulisan kedua yang juga mirip tulisan pertama semoga bisa terlihat"
    ]
    async def token_generator(): 
        for word in ["Hello", "there,", "this", "is", "streamed.","Hello", "there,", "this", "is", "streamed.","Hello", "there,", "this", "is", "streamed."]: 
            #yield f"data: {word}\n\n" 
            #await asyncio.sleep(0.5)
            for char in word:
                yield f"{char}"
                await asyncio.sleep(0.05)
            yield f" "

    return EventSourceResponse(StreamCharWriter(arr))

@app.get("/welcome")
async def welcome_process():
    message = welcome()
    return EventSourceResponse(StreamCharWriter(message.processed))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)