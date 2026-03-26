from flask import Flask, request, jsonify
from predictor import predict_disease
from ollama_ai import generate_explanation
from flask import Flask, request, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return "Heartbeat AI Backend Running"


@app.route("/analyze", methods=["POST"])
def analyze():
    print("Request received")
    data = request.json
    bpm = data["bpm"]

    prediction = predict_disease(bpm)

    try:
        explanation = generate_explanation(bpm, prediction["condition"])
    except Exception as e:
        print("AI error:", e)
        explanation = "AI explanation unavailable"

    return jsonify({
        "bpm": bpm,
        "condition": prediction["condition"],
        "severity": prediction["severity"],
        "ai_explanation": explanation
    })


if __name__ == "__main__":
    app.run(debug=True)