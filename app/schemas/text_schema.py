from pydantic import BaseModel
from typing import List

class TextRequest(BaseModel):
    texts: str

class TextResponse(BaseModel):
    processed: List[str]