async function analyzeHeartbeat() {
    console.log("Analyze button clicked");
    let bpm = document.getElementById("bpm").value;

    if (!bpm || bpm < 40 || bpm > 200) {
        alert("Please enter a valid BPM between 40 and 200.");
        return;
    }

    // Show loading
    const button = document.querySelector("button");
    const originalText = button.innerText;
    button.innerText = "Analyzing...";
    button.disabled = true;

    try {
        let response = await fetch("http://127.0.0.1:5000/analyze", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                bpm: bpm
            })
        });

        let data = await response.json();

        document.getElementById("condition").innerText = data.condition;
        document.getElementById("severity").innerText = data.severity;
        document.getElementById("explanation").innerText = data.ai_explanation;

        // Show result section
        document.getElementById("result-section").style.display = "block";
    } catch (error) {
        alert("Error analyzing heartbeat. Please try again.");
        console.error(error);
    } finally {
        // Reset button
        button.innerText = originalText;
        button.disabled = false;
    }
}