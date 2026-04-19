// ---------------- BMI CALCULATION ----------------
function calculateBMI(){
    let height = document.getElementById("height")?.value;
    let weight = document.getElementById("weight")?.value;

    if(height && weight){
        let bmi = weight / ((height/100)*(height/100));
        document.getElementById("bmi").value = bmi.toFixed(2);
    }
}

if(document.getElementById("height")){
    document.getElementById("height").addEventListener("input", calculateBMI);
    document.getElementById("weight").addEventListener("input", calculateBMI);
}

// ---------------- LOGIN ----------------
function loginUser(){
    let email = document.getElementById("loginEmail").value;
    let password = document.getElementById("loginPassword").value;

    fetch("http://127.0.0.1:5000/login", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({email, password})
    })
    .then(res => res.json())
    .then(data => {
        if(data.status === "success"){
            localStorage.setItem("userEmail", email);
            alert("Login successful");
            window.location.href = "assessment.html";
        } else {
            alert(data.message);
        }
    })
    .catch(() => alert("Server error"));
}

// ---------------- SIGNUP ----------------
function signupUser(){
    let email = document.getElementById("signupEmail").value;
    let password = document.getElementById("signupPassword").value;

    if(!email || !password){
        alert("Please fill all fields");
        return;
    }

    fetch("http://127.0.0.1:5000/signup", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({email, password})
    })
    .then(res => res.json())
    .then(data => {
        if(data.status === "success"){
            alert("Signup successful!");
            window.location.href = "login.html";
        } else {
            alert(data.message || "Signup failed");
        }
    })
    .catch(() => alert("Server error"));
}

// ---------------- LOGOUT ----------------
function logoutUser(){
    localStorage.clear();
    window.location.href = "login.html";
}

// ---------------- MAIN AI PREDICTION ----------------
async function predictAll() {
    try {

        // 📥 GET RAW INPUT VALUES
        let ageInput = document.getElementById("age");
        let bmiInput = document.getElementById("bmi");
        let bpInput = document.getElementById("bp");
        let glucoseInput = document.getElementById("glucose");
        let cholesterolInput = document.getElementById("cholesterol");

        let age = ageInput.value;
        let bmi = bmiInput.value;
        let bp = bpInput.value;
        let glucose = glucoseInput.value;
        let cholesterol = cholesterolInput.value;

        // 🚫 VALIDATION (EMPTY CHECK)
        let inputs = [ageInput, bmiInput, bpInput, glucoseInput, cholesterolInput];
        let hasError = false;

        inputs.forEach(input => {
            if (!input.value) {
                input.style.border = "2px solid red";
                hasError = true;
            } else {
                input.style.border = "1px solid #ccc";
            }
        });

        if (hasError) {
            alert(" Please fill all fields!");
            return;
        }

        // ✅ CONVERT TO NUMBER
        age = parseFloat(age);
        bmi = parseFloat(bmi);
        bp = parseFloat(bp);
        glucose = parseFloat(glucose);
        cholesterol = parseFloat(cholesterol);

        console.log("Sending:", age, bmi, bp, glucose, cholesterol);

        // 🌐 API CALL
        let res = await fetch("http://127.0.0.1:5000/predict_all", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                age,
                bmi,
                bp,
                glucose,
                cholesterol
            })
        });

        let data = await res.json();
        console.log("BACKEND RESPONSE:", data);

        // ❌ ERROR CHECK
        if (data.error) {
            alert("Backend Error: " + data.error);
            return;
        }

        // ✅ EXTRACT RESULT
        let disease = data.disease || "Unknown";
        let risk = data.risk || "Low Risk";

        // 💾 SAVE FOR DASHBOARD
        localStorage.setItem("disease", disease);
        localStorage.setItem("risk", risk);
        localStorage.setItem("lastDisease", disease);
        localStorage.setItem("lastRisk", risk);

        // 🎨 COLOR LOGIC
        let color = "green";
        if (risk === "Medium Risk") color = "orange";
        if (risk === "High Risk") color = "red";

        // 🧾 RESULT UI
        document.getElementById("result").innerHTML = `
            <div class="result-card" style="border-left: 6px solid ${color}">
                <h2> ${disease}</h2>
                <p style="color:${color}; font-weight:bold;">${risk}</p>
            </div>
        `;

        // 💡 SUGGESTIONS
        let suggestionText = "";

        if (risk === "High Risk") {
            suggestionText = " Consult doctor immediately.";
        } else if (risk === "Medium Risk") {
            suggestionText = " Improve diet and exercise.";
        } else {
            suggestionText = " You are healthy!";
        }

        document.getElementById("suggestions").innerHTML = `
            <div class="suggestion-box">${suggestionText}</div>
        `;

        // 🔁 AUTO REDIRECT (ONLY AFTER SUCCESS)
        setTimeout(() => {
            window.location.href = "dashboard.html";
        }, 1500);

    } 
    catch (err) {
        console.error("FULL ERROR:", err);
        alert("Server error: " + err);
    }
}
// TOGGLE CHAT
// TOGGLE
function toggleChatbot(){
    let box = document.getElementById("chatbotBox");
    box.style.display = box.style.display === "flex" ? "none" : "flex";
}

// SEND MESSAGE
function sendMessage(){

    let input = document.getElementById("chatInput");
    let message = input.value.trim();

    if(message === "") return;

    let chatBody = document.getElementById("chatBody");

    // USER MESSAGE
    chatBody.innerHTML += `<div class="user-msg">${message}</div>`;

    input.value = "";

    // THINKING EFFECT
    chatBody.innerHTML += `<div class="bot-msg">Typing...</div>`;

    setTimeout(() => {

        chatBody.lastChild.remove();

        let reply = getSmartReply(message);

        chatBody.innerHTML += `<div class="bot-msg">${reply}</div>`;
        chatBody.scrollTop = chatBody.scrollHeight;

    }, 700);
}


// 🧠 SMART LOGIC (FEELS LIKE AI)
function getSmartReply(msg){

    msg = msg.toLowerCase();

    let disease = localStorage.getItem("lastDisease");
    let risk = localStorage.getItem("lastRisk");

    // GREETING
    if(msg.includes("hello") || msg.includes("hi")){
        return "Hello  I can analyze your health and give smart suggestions!";
    }

    // ASK RESULT
    if(msg.includes("my result") || msg.includes("my health")){
        if(disease){
            return `Your latest prediction shows ${disease} with ${risk}.`;
        }
        else{
            return "Please run health check first ";
        }
    }

    // ADVICE BASED ON RESULT
    if(msg.includes("what should i do") || msg.includes("advice")){
        if(!disease) return "Please check your health first.";

        if(risk === "High Risk"){
            return ` You may have ${disease}. I strongly suggest consulting a doctor and improving lifestyle immediately.`;
        }
        else if(risk === "Medium Risk"){
            return ` You have moderate risk of ${disease}. Focus on diet, exercise and monitoring.`;
        }
        else{
            return ` Your risk is low. Maintain your healthy lifestyle.`;
        }
    }

    // DISEASE SPECIFIC
    if(msg.includes("diabetes")){
        return "Control sugar intake, exercise daily, and monitor glucose.";
    }

    if(msg.includes("heart")){
        return "Maintain low cholesterol, regular exercise, and stress control.";
    }

    // DEFAULT SMART
    return "I can help you understand your health report. Try asking: 'my result' or 'what should I do?' ";
}
