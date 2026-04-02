import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from src.main.routers import physics_solver_router
from src.main.core import settings, logger

app = FastAPI(title="Physics Solver API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(physics_solver_router)

@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {"message": "Physics Solver API is running. Send a POST request to /solve."}

if __name__ == "__main__":
    port = settings.PORT
    
    logger.info(f"Starting server on http://localhost:{port}")
    uvicorn.run("main:app", host="127.0.0.1", port=port, reload=True)