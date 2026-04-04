import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))
try:
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents="hello"
    )
    print("Success:", response.text)
except Exception as e:
    print("Error:", e)
