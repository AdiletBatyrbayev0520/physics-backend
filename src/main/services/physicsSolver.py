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
        
        Requirements:
        1. Provide a concise and catchy title for the problem.
        2. Identify the core subject. 
        3. Assign a difficulty level.
        4. Extract the known variables. For each:
           - 'name': The mathematical symbol (e.g., 'q_1', 'R', '\\mu_0').
           - 'value': The numerical value and unit (e.g., '4.0 \\times 10^{{-9}} \\text{{ C }}', '120 \\text{{ m }}').
           - 'description': What it represents (e.g., 'Initial charge', 'Radius').
        5. Break down the solution into steps with titles, content, and RAW LaTeX (without delimiters like $ or \\( ).
        6. Provide a final numerical answer. Use RAW LaTeX for the 'value' field.
        7. IMPORTANT LaTeX RULES: 
           - For 'name', 'value', and 'math' fields, use RAW LaTeX without delimiters. 
           - NEVER include \\\\ or \\newline at the end of a formula.
           - In display math/BlockMath, avoid using \\\\ unless you are inside an environment like 'aligned'.
           - Keep LaTeX pure and symbolic. Put descriptive text in 'description' or 'content' fields.
        8. Pay strict attention to units and significant figures.
        
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
        
        1. Extract the problem statement from the image and use it as the description.
        2. Provide a concise and catchy title for the problem.
        3. Identify the core subject. 
        4. Assign a difficulty level.
        5. Extract the known variables. Use 'name' for the symbol, 'value' for the value/unit, and 'description' for the text description.
        6. Break down the solution into clear, logical steps with titles, content, and RAW LaTeX (without delimiters).
        7. Provide a final numerical answer. Use RAW LaTeX for the 'value' field.
        8. IMPORTANT: For ALL 'name', 'value', and 'math' fields, use RAW LaTeX. Do NOT use \\\\ or \\newline at the end of a formula.
        9. Pay strict attention to units, unit conversions, and significant figures.
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
