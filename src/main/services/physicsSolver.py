import os
from google import genai
from google.genai import types
from src.main.core import logger, settings
from src.main.models import PhysicsSolution


class PhysicsSolverAgent:
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model_id = 'gemini-2.5-flash'
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
        logger.info("Successfully generated physics solution from text.")
        return solution

    def solve_with_image(self, image_bytes: bytes, mime_type: str, custom_prompt: str = "") -> PhysicsSolution:
        logger.info("Analyzing and solving physics problem from image...")
        
        default_prompt = """
        You are an expert university physics professor. 
        An image of a physics problem is provided. 
        1. Extract the problem statement from the image.
        2. Solve it carefully, paying strict attention to units and significant figures.
        """
        
        prompt = custom_prompt if custom_prompt else default_prompt
        
        image_part = types.Part.from_bytes(
            data=image_bytes,
            mime_type=mime_type
        )
        
        response = self.client.models.generate_content(
            model=self.model_id,
            contents=[prompt, image_part],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=PhysicsSolution,
                temperature=0.1,
            ),
        )
        
        solution = PhysicsSolution.model_validate_json(response.text)
        logger.info("Successfully generated physics solution from image.")
        return solution


