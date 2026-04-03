// ==============================
// Prediction Function
// ==============================

async function predict() {

    const features = [
        parseFloat(document.getElementById("age").value),
        parseFloat(document.getElementById("sex").value),
        parseFloat(document.getElementById("cp").value),
        parseFloat(document.getElementById("trestbps").value),
        parseFloat(document.getElementById("chol").value),
        parseFloat(document.getElementById("fbs").value),
        parseFloat(document.getElementById("restecg").value),
        parseFloat(document.getElementById("thalach").value),
        parseFloat(document.getElementById("exang").value),
        parseFloat(document.getElementById("oldpeak").value),
        parseFloat(document.getElementById("slope").value),
        parseFloat(document.getElementById("ca").value),
        parseFloat(document.getElementById("thal").value)
    ];

    try {

        const response = await fetch("http://127.0.0.1:5000/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ features: features })
        });

        const data = await response.json();

        const resultText =
            data.prediction === 1
                ? "⚠️ Heart Disease Risk Detected"
                : "✅ No Heart Disease Detected";

        document.getElementById("result-container").style.display = "block";
        document.getElementById("result").innerText = resultText;

        document.getElementById("explanation").innerText =
            data.explanation;

        // Show chat button after prediction
        document.getElementById("chatBtn").style.display = "block";

    } catch (error) {

        console.error("Prediction error:", error);
        alert("Error connecting to backend.");

    }
}


// ==============================
// Chat Toggle
// ==============================

function showChat() {

    document.getElementById("chatSection").style.display = "block";

}



// ==============================
// Send Chat Message
// ==============================

async function sendMessage() {

    const inputField = document.getElementById("userInput");

    const message = inputField.value.trim();

    if (message === "") return;

    const chatbox = document.getElementById("chatbox");

    // Show user message
    chatbox.innerHTML +=
        "<p class='msg-user'><b>You:</b> " + message + "</p>";

    inputField.value = "";

    try {

        const response = await fetch("http://127.0.0.1:5000/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message
            })

        });

        const data = await response.json();

        // Show AI response
        chatbox.innerHTML +=
            "<p class='msg-ai'><b>AI Doctor:</b> " + data.response + "</p>";

        // Auto scroll
        chatbox.scrollTop = chatbox.scrollHeight;

    } catch (error) {

        console.error("Chat error:", error);

        chatbox.innerHTML +=
            "<p class='msg-ai'><b>AI Doctor:</b> Unable to connect to AI system.</p>";

    }
}



// ==============================
// Enter Key Support
// ==============================

document.addEventListener("DOMContentLoaded", function () {

    const input = document.getElementById("userInput");

    if (input) {

        input.addEventListener("keypress", function (event) {

            if (event.key === "Enter") {

                sendMessage();

            }

        });

    }

});