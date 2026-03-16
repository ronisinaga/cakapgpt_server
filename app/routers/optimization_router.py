from fastapi import APIRouter
from sse_starlette import EventSourceResponse
from app.schemas.text_schema import TextRequest
from app.controllers.optimization_controller import create_session,create_objective_function,fetch_fungsi_kendala,create_kendala_session,solution_optimization

optimization_router = APIRouter()

@optimization_router.post("/optsession")
async def optimization_session(req:TextRequest):
    return create_session(req.texts)

@optimization_router.post("/sessionkendala")
async def kendala_session_create(req:TextRequest):
    return create_kendala_session(req.texts)

@optimization_router.get("/objective")
async def objective(session:str):
    stream = create_objective_function(session)
    return EventSourceResponse(
        stream,
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "http://localhost:5173"
        }
    )

@optimization_router.get("/fungsikendala")
async def get_fungsi_kendala(session:str):
    stream = fetch_fungsi_kendala(session)
    return EventSourceResponse(
        stream
    )

@optimization_router.get("/soloptimization")
async def optimization_solution(sessionOb:str,sessionK:str,prompt:str):
    stream = solution_optimization(sessionOb,sessionK,prompt)
    return EventSourceResponse(
        stream
    )