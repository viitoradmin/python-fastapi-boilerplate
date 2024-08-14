from typing import List
from pydantic import BaseModel

class Step(BaseModel):
    explanation: str
    output: str

class MathResponse(BaseModel):
    steps: List[Step]
    final_answer: str