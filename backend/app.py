import os
import sys

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from flask import Flask, request, jsonify
from flask_cors import CORS
from models.predict_model import predict_heart_risk as predict
from rag.rag_engine import RAGEngine
from backend.gemini_ai import ask_gemini, extract_medical_data_from_document

app = Flask(__name__, static_folder='../frontend', static_url_path='/')
CORS(app)

@app.route("/")
def index():
    return app.send_static_file("index.html")

rag = RAGEngine()

# -----------------------
# Prediction API
# -----------------------
@app.route("/predict", methods=["POST"])
def predict_route():

    data = request.json
    features = data["features"]

    prediction = predict(features)

    explanation = rag.generate_explanation(prediction)

    feature_names = [
        "Age", "Sex (1=M, 0=F)", "Chest Pain (0-3)", "Resting Blood Pressure", 
        "Cholesterol", "Fasting Blood Sugar > 120", "Resting ECG (0-2)", 
        "Max Heart Rate", "Exercise Angina (1/0)", "ST Depression", 
        "Slope (0-2)", "Major Vessels (0-3)", "Thalassemia (1-3)"
    ]
    try:
        patient_info_lines = []
        for name, val in zip(feature_names, features):
            display_val = val if val is not None else "Not Provided (Estimated by AI)"
            patient_info_lines.append(f"{name}: {display_val}")
        patient_info = "\n".join(patient_info_lines)
        prompt = f"""
Based on the following patient health features:
{patient_info}

What are the top 3 heart-related diseases or conditions this patient might be at risk for? Include an estimated probability percentage for each. Keep the response brief and formatted as bullet points.
"""
        top_diseases = ask_gemini(prompt)
    except Exception as e:
        top_diseases = "Could not fetch top 3 diseases."

    return jsonify({
        "prediction": prediction,
        "explanation": explanation,
        "top_diseases": top_diseases
    })


# -----------------------
# Chat API
# -----------------------
@app.route("/chat", methods=["POST"])
def chat():

    data = request.json
    message = data["message"]

    context = rag.get_context(message)

    prompt = f"""
You are an AI cardiology assistant.

User question:
{message}

Medical context:
{context}

Provide a helpful answer. Always format your answer using bullet points for clarity.
"""

    response = ask_gemini(prompt)

    return jsonify({
        "response": response
    })


# -----------------------
# Document Upload API
# -----------------------
@app.route("/upload-document", methods=["POST"])
def upload_document():
    if 'document' not in request.files:
        return jsonify({"error": "No document provided"}), 400
        
    file = request.files['document']
    
    if file.filename == '':
        return jsonify({"error": "No document selected"}), 400
        
    try:
        file_bytes = file.read()
        mime_type = file.mimetype
        
        # Default to pdf or image types
        if mime_type not in ["application/pdf", "image/jpeg", "image/png", "image/webp", "image/jpg"]:
            mime_type = "application/pdf" # fallback
            
        extracted_data = extract_medical_data_from_document(file_bytes, mime_type)
        
        return jsonify({
            "message": "Extracted successfully",
            "extracted_data": extracted_data
        })
    except Exception as e:
        print(f"Error processing file: {e}")
        return jsonify({"error": "Failed to process document"}), 500


if __name__ == "__main__":
    app.run(debug=True)