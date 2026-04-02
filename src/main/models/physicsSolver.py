from pydantic import BaseModel, Field

class Variable(BaseModel):
    name: str = Field(
        description="Name of the variable (e.g., 'q', 'r', 'ΔV')"
    )
    value: str = Field(
        description="Value of the variable including units (e.g., '+3.0 nC', '0.20 m')"
    )

class PhysicsSolution(BaseModel):
    problem_statement: str = Field(
        description="The original problem text."
    )
    known_variables: list[Variable] = Field(
        description="List of given variables and their values."
    )
    formulas_used: list[str] = Field(
        description="Core physics formulas needed for the solution (e.g., ['E = k * |q| / r^2'])."
    )
    step_by_step_solution: str = Field(
        description="Detailed, step-by-step mathematical derivations and calculations. Explain the physics reasoning clearly."
    )
    final_answer: str = Field(
        description="The final numerical answer with appropriate units and significant figures."
    )

class ProblemRequest(BaseModel):
    problem_text: str = Field(
        ..., 
        example="A point charge q = +3.0 nC. Find the electric field magnitude E at a distance r = 0.20 m."
    )