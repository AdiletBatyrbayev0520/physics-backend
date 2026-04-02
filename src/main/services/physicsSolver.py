import os
from google import genai
from google.genai import types
from src.main.core import logger, settings
from src.main.models import PhysicsSolution


class PhysicsSolverAgent:
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model_id = 'gemini-2.5-pro'
        logger.info(f"Initialized PhysicsSolverAgent with model: {self.model_id}")

    def solve(self, problem_text: str) -> PhysicsSolution:
        logger.info(f"Analyzing and solving problem: {problem_text[:50]}...")
        
        prompt = f"""
        You are an expert university physics professor. 
        Solve the following physics problem carefully. 
        Pay strict attention to units, unit conversions (e.g., nC to C, cm to m), and significant figures.
        
        Problem:
        {problem_text}
        """

        response = self.client.models.generate_content(
            model=self.model_id,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=PhysicsSolution,
                temperature=0.1, 
            ),
        )
        
        solution = PhysicsSolution.model_validate_json(response.text)
        logger.info("Successfully generated physics solution.")
        return solution


