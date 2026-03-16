from pydantic import BaseModel
from typing import List

class LinearEquationRequest(BaseModel):
    equations: List[str]
    method: str

class LinearEquationResponse(BaseModel):
    equations: List[str]         # array of string
    vector: List[int]            # numeric vector
    matrix: List[List[int]]      # numeric matrix
    result: str                  # string of result