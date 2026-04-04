import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

# Create the client
client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))

def ask_gemini(prompt: str) -> str:
    """Send a prompt to Gemini and return the text response."""
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )
    return response.text

def generate_explanation(bpm: int, condition: str) -> str:
    """Generate a simple explanation for the health risk."""
    prompt = f"""
    A patient has a heart rate of {bpm} BPM.
    The predicted condition is {condition}.
    Explain the possible health risk in 2 simple sentences.
    """
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )
    return response.text
