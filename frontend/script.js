// ==============================
// Prediction Function
// ==============================

async function predict() {

    const getVal = (id) => {
        let val = document.getElementById(id).value.trim();
        return val === "" ? null : parseFloat(val);
    };

    const features = [
        getVal("age"),
        getVal("sex"),
        getVal("cp"),
        getVal("trestbps"),
        getVal("chol"),
        getVal("fbs"),
        getVal("restecg"),
        getVal("thalach"),
        getVal("exang"),
        getVal("oldpeak"),
        getVal("slope"),
        getVal("ca"),
        getVal("thal")
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

        if (data.top_diseases) {
            let formattedDiseases = data.top_diseases.replace(/\*\*(.*?)\*\*/g, '<b>$1</b>').replace(/\n/g, '<br>');
            document.getElementById("top-diseases").innerHTML = "<h3>Top 3 Disease Risks:</h3>" + formattedDiseases;
        }

    } catch (error) {

        console.error("Prediction error:", error);
        alert("Error connecting to backend.");

    }
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

        let formattedResponse = data.response.replace(/\*\*(.*?)\*\*/g, '<b>$1</b>').replace(/\n/g, '<br>');
        // Show AI response
        chatbox.innerHTML +=
            "<p class='msg-ai'><b>AI Doctor:</b><br>" + formattedResponse + "</p>";

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