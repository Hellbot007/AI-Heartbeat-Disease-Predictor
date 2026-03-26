from flask import Flask, request, jsonify
from predictor import predict_disease
from ollama_ai import generate_explanation

app = Flask(__name__)

@app.route("/")
def home():
    return "Heartbeat AI Backend Running"


@app.route("/analyze", methods=["POST"])
def analyze():

    data = request.json
    bpm = data["bpm"]

    prediction = predict_disease(bpm)

    explanation = generate_explanation(
        bpm,
        prediction["condition"]
    )

    return jsonify({
        "bpm": bpm,
        "condition": prediction["condition"],
        "severity": prediction["severity"],
        "ai_explanation": explanation
    })


if __name__ == "__main__":
    app.run(debug=True)