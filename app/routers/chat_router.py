from fastapi import APIRouter
from sse_starlette import EventSourceResponse
from app.helpers.StreamWriterHelper import StreamCharWriter, StreamWordWriter
from app.controllers.chat_controller import welcome,choice

chat_router = APIRouter()

@chat_router.get("/welcome")
async def welcome_router():
    message = welcome()
    return EventSourceResponse(StreamWordWriter(message.processed),
        headers={
            "Access-Control-Allow-Origin": "http://localhost:5173",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        })

@chat_router.get("/chat")
async def chat(input:str):
    mes = choice(input)
    return EventSourceResponse(StreamWordWriter(mes.message),
        headers={
            "Access-Control-Allow-Origin": "http://localhost:5173",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        })