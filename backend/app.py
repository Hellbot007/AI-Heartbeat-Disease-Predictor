import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from flask import Flask, request, jsonify
from backend.predictor import predict
from rag.rag_engine import RAGEngine
from backend.gemini_ai import ask_gemini

app = Flask(__name__)

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

    return jsonify({
        "prediction": prediction,
        "explanation": explanation
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

Provide a helpful answer.
"""

    response = ask_gemini(prompt)

    return jsonify({
        "response": response
    })


if __name__ == "__main__":
    app.run(debug=True)