import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure the API key
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

# Create the model instance using the standard robust and fast model
model = genai.GenerativeModel('gemini-1.5-flash')

def ask_gemini(prompt: str) -> str:
    """Send a prompt to Gemini and return the text response."""
    response = model.generate_content(prompt)
    return response.text

def generate_explanation(bpm: int, condition: str) -> str:
    """Generate a simple explanation for the health risk."""
    prompt = f"""
    A patient has a heart rate of {bpm} BPM.
    The predicted condition is {condition}.
    Explain the possible health risk in 2 simple sentences.
    """
    response = model.generate_content(prompt)
    return response.text
