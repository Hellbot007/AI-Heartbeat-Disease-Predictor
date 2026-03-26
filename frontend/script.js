async function analyzeHeartbeat(){
console.log("Analyze button clicked");
let bpm = document.getElementById("bpm").value;

let response = await fetch("http://127.0.0.1:5000/analyze", {

method: "POST",

headers:{
"Content-Type":"application/json"
},

body: JSON.stringify({
bpm:bpm
})

});

let data = await response.json();

document.getElementById("condition").innerText =
"Condition: " + data.condition;

document.getElementById("severity").innerText =
"Severity: " + data.severity;

document.getElementById("explanation").innerText =
"AI Explanation: " + data.ai_explanation;

}