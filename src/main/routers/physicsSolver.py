from src.main.services import PhysicsSolverAgent
from src.main.models import PhysicsSolution, ProblemRequest
from src.main.core import logger
from fastapi import APIRouter, HTTPException

router = APIRouter()
agent = PhysicsSolverAgent()

@router.post("/solve", response_model=PhysicsSolution)
async def solve_problem(request: ProblemRequest):
    logger.info(f"Received request to solve problem: {request.problem_text[:50]}...")
    try:
        solution = agent.solve(request.problem_text)
        return solution
    except Exception as e:
        logger.error(f"Error solving physics problem: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


