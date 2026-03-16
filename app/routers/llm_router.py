import json
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from sse_starlette import EventSourceResponse

from app.controllers.llm_controller import chatGPT,startChat
from app.helpers.StreamWriterHelper import StreamWordWriter,StreamTextWriter
from app.libs.llm.Gemini import stream_chat
from app.schemas.llm_schema import ChatRequest, ChatResponse

llm_router = APIRouter()

@llm_router.post("/chat/openai", response_model=ChatResponse)
def chat(req:ChatRequest):
    reply = chatGPT(req.messages)
    return {"reply": reply}

@llm_router.post("/chat/gemini", response_model=ChatResponse)
def chat(req:ChatRequest):
    def event_generator():
        for token in stream_chat(req.messages):
            yield token

    return StreamingResponse(
        event_generator(),
        media_type="text/plain"
    )

@llm_router.get("/chat/stream")
def chat(prompt:str):
    json_string = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }, ensure_ascii=False)
    chat = startChat(json_string)
    if isinstance(chat,str):
        chat = [chat]
    return EventSourceResponse(startChat(json_string),
        headers={
            "Access-Control-Allow-Origin": "http://localhost:5173",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        })

@llm_router.get("/chat/start")
async def start():
    #return create_session(req.texts)
    json_string = """
        {
        "messages": [
            {
            "role": "user",
            "content": "Aku ingin berdiskusi dengan kamu"
            }
        ]
        }
    """
    welcome = startChat(json_string)
    return EventSourceResponse(startChat(json_string),
        headers={
            "Access-Control-Allow-Origin": "http://localhost:5173",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        })