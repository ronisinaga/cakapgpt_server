from fastapi import APIRouter
from sse_starlette import EventSourceResponse
from app.schemas.text_schema import TextRequest
from app.helpers.StreamWriterHelper import StreamCharOfTextWriter,StreamCharWriter,StreamDoneWriter
from app.controllers.experiment_controller import create_session

experiment_router = APIRouter()

@experiment_router.get("/experiment")
async def experiment():
    #return create_session(req.texts)
    stream = create_session()
    return EventSourceResponse(
        stream,
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "http://localhost:5173"
        }
    )