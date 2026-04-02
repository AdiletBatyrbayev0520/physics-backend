import random
import string
import time
from typing import Optional
from pydantic import BaseModel, Field

class Variable(BaseModel):
    name: str = Field(
        description="Symbol of the variable (e.g., 'q', 'r', 'ΔV')"
    )
    value: str = Field(
        description="Value of the variable including units (e.g., '+3.0 nC', '0.20 m')"
    )
    description: str = Field(
        description="Brief description of what this variable represents."
    )

class ProblemStep(BaseModel):
    title: str
    content: str
    math: Optional[str] = None

class FinalAnswer(BaseModel):
    value: str
    unit: str
    explanation: str

class PhysicsSolution(BaseModel):
    id: str = Field(default_factory=lambda: "sol_" + "".join(random.choices(string.ascii_lowercase + string.digits, k=8)))
    title: str
    description: str
    subject: str
    difficulty: str
    timestamp: float = Field(default_factory=lambda: time.time() * 1000)
    known_variables: list[Variable] = Field(default_factory=list)
    steps: list[ProblemStep]
    final_answer: FinalAnswer

class ProblemRequest(BaseModel):
    problem_text: str = Field(
        ..., 
        example="A point charge q = +3.0 nC. Find the electric field magnitude E at a distance r = 0.20 m."
    )