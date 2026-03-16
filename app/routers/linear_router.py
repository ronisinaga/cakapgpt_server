from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from sse_starlette import EventSourceResponse
from app.controllers.linear_controller import solution_linear,linear_solution,create_session,receive_linear
from app.schemas.linear_equation_schema import LinearEquationResponse, LinearEquationRequest
from app.helpers.StreamWriterHelper import StreamCharWriter,StreamCharOfTextWriter
from app.schemas.text_schema import TextRequest

linear_router = APIRouter()
    

@linear_router.post("/equation")
async def linear_process(req:LinearEquationRequest):
    solution = solution_linear(req.equations,req.method)
    return StreamingResponse(
        StreamCharWriter(solution.equations),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "http://localhost:5173"
        }
)

@linear_router.get("/linearsolution")
async def linear_result(session:str,method:str):
    solution = linear_solution(session,method)
    return EventSourceResponse(solution)


@linear_router.post("/linsession")
async def linear_session(req:TextRequest):
    return create_session(req.texts)


@linear_router.get("/linearequation")
async def linear_format(session:str):
    stream = await receive_linear(session)
    return EventSourceResponse(
        stream,
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )