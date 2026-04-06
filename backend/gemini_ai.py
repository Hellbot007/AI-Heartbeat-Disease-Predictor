import os
import json
from google import genai
from google.genai import types
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

def extract_medical_data_from_document(file_bytes: bytes, mime_type: str) -> dict:
    """Uses Gemini multimodal features to extract health data from a file into structured JSON."""
    prompt = """
    Analyze this medical document and extract the following patient values. 
    Format the response STRICTLY as a JSON object with these exact keys and format:
    "age": integer (years)
    "sex": 1 for male, 0 for female
    "cp": Chest Pain Type (0-3)
    "trestbps": Resting Blood Pressure (systolic, mm Hg)
    "chol": Serum Cholesterol in mg/dl
    "fbs": Fasting Blood Sugar (1 if >120 mg/dl, 0 otherwise)
    "restecg": Resting ECG Results (0-2)
    "thalach": Max Heart Rate achieved
    "exang": Exercise Angina (1 for Yes, 0 for No)
    "oldpeak": ST Depression (Oldpeak) (numeric/float)
    "slope": Peak Exercise ST Segment (0-2)
    "ca": Major Vessels (0-3)
    "thal": Thalassemia (1-3)

    If a value is not explicitly stated or cannot be confidently inferred, set its value to null.
    Do not add any markup, explanation or extra details. Output valid JSON ONLY.
    """
    
    try:
        document_part = types.Part.from_bytes(data=file_bytes, mime_type=mime_type)
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[document_part, prompt],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            )
        )
        
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]
            
        return json.loads(text.strip())
        
    except Exception as e:
        print(f"Error extracting data: {e}")
        return {}
