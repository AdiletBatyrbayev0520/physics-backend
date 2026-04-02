from src.main.services import PhysicsSolverAgent
from src.main.models import PhysicsSolution, ProblemRequest, ImageProblemRequest
from src.main.core import logger
from fastapi import APIRouter, HTTPException
from typing import Optional

router = APIRouter()
agent = PhysicsSolverAgent()

@router.post("/solve/text", response_model=PhysicsSolution)
async def solve_problem(request: ProblemRequest):
    logger.info(f"Received request to solve problem: {request.problem_text[:50]}...")
    try:
        solution = agent.solve(request.problem_text)
        return solution
    except Exception as e:
        logger.error(f"Error solving physics problem: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/solve/image", response_model=PhysicsSolution)
async def solve_problem_image(
    request: ImageProblemRequest
):
    logger.info(f"Received image solving request. File: {request.file.filename}, Content-type: {request.file.content_type}")
    
    if not request.file.content_type.startswith("image/"):
        logger.warning(f"Invalid file type: {request.file.content_type}")
        raise HTTPException(status_code=400, detail="File must be an image.")
    
    try:
        image_bytes = await request.file.read()
        solution = agent.solve_with_image(
            image_bytes=image_bytes,
            mime_type=request.file.content_type,
            custom_prompt=request.prompt
        )
        return solution
    except Exception as e:
        logger.error(f"Error solving physics problem from image: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


