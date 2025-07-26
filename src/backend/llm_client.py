import os
import json
from typing import Dict, Any, Optional
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class LLMClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("No Gemini API key provided")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def chat(self, prompt: str, system: str = "") -> str:
        """Simple chat completion"""
        try:
            full_prompt = f"{system}\n\n{prompt}" if system else prompt
            response = self.model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            print(f"Error in chat completion: {e}")
            return f"Error: {str(e)}"
    
    def structured_chat(self, prompt: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        """Get structured JSON response"""
        try:
            json_prompt = f"""
            {prompt}
            
            Please respond with valid JSON that matches this schema:
            {json.dumps(schema, indent=2)}
            
            IMPORTANT: Return ONLY valid JSON, no other text.
            """
            
            response = self.model.generate_content(json_prompt)
            
            # Try to parse JSON from response
            try:
                return json.loads(response.text.strip())
            except json.JSONDecodeError:
                # If direct parsing fails, try to extract JSON from response
                text = response.text.strip()
                if text.startswith('```json'):
                    text = text[7:]
                if text.endswith('```'):
                    text = text[:-3]
                return json.loads(text.strip())
                
        except Exception as e:
            print(f"Error in structured chat: {e}")
            # Return empty structure matching schema
            return self._empty_response_for_schema(schema)
    
    def _empty_response_for_schema(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        """Generate empty response matching schema structure"""
        result = {}
        for key, value in schema.items():
            if isinstance(value, dict):
                result[key] = self._empty_response_for_schema(value)
            elif isinstance(value, list):
                result[key] = []
            elif isinstance(value, str):
                result[key] = ""
            elif isinstance(value, int):
                result[key] = 0
            elif isinstance(value, bool):
                result[key] = False
            else:
                result[key] = None
        return result