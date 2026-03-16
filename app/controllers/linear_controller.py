from app.schemas.text_schema import TextResponse, TextRequest
from app.services.linear_service import linear_solution,sessionid,receive_linear_input,solution
from app.schemas.linear_equation_schema import LinearEquationResponse

def solution_linear(equations,method) -> LinearEquationResponse:
    result = solution(equations,method)
    
    return LinearEquationResponse(
        equations=result["equations"],
        matrix= result["matrix"],
        vector= result["vector"],
        result= result["solution"]
    )

def linear_solution(session,method):
    return solution(session,method)

def create_session(req):
    return sessionid(req)

async def receive_linear(session):
    return receive_linear_input(session)
