from pydantic import BaseModel
from typing import List

class ChoiceResponse(BaseModel):
    status: bool
    message: List[str]