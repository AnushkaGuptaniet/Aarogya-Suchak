from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import pickle
import sqlite3

app = Flask(**name**)
CORS(app)

# ---------------- LOAD MODELS ----------------

# (make sure models folder exists in your repo)

diabetes_model = pickle.load(open("models/diabetes.pkl", "rb"))
heart_model = pickle.load(open("models/heart.pkl", "rb"))
liver_model = pickle.load(open("models/liver.pkl", "rb"))
kidney_model = pickle.load(open("models/kidney.pkl", "rb"))

# ==========================

# 🔥 DISEASE LOGIC FUNCTIONS

# ==========================

def get_diabetes_result(data):
glucose = float(data.get("glucose", 0))

```
if glucose > 200:
    return {"disease": "Diabetes", "risk": "High Risk", "score": 0.9}
elif glucose > 140:
    return {"disease": "Diabetes", "risk": "Medium Risk", "score": 0.6}
else:
    return {"disease": "Diabetes", "risk": "Low Risk", "score": 0.2}
```

def get_heart_result(data):
bp = float(data.get("bp", 0))

```
if bp > 170:
    return {"disease": "Heart Disease", "risk": "High Risk", "score": 0.85}
elif bp > 130:
    return {"disease": "Heart Disease", "risk": "Medium Risk", "score": 0.6}
else:
    return {"disease": "Heart Disease", "risk": "Low Risk", "score": 0.2}
```

def get_liver_result(data):
chol = float(data.get("cholesterol", 0))

```
if chol > 300:
    return {"disease": "Liver Disease", "risk": "High Risk", "score": 0.8}
elif chol > 200:
    return {"disease": "Liver Disease", "risk": "Medium Risk", "score": 0.5}
else:
    return {"disease": "Liver Disease", "risk": "Low Risk", "score": 0.2}
```

def get_kidney_result(data):
age = float(data.get("age", 0))

```
if age > 60:
    return {"disease": "Kidney Disease", "risk": "High Risk", "score": 0.75}
elif age > 40:
    return {"disease": "Kidney Disease", "risk": "Medium Risk", "score": 0.5}
else:
    return {"disease": "Kidney Disease", "risk": "Low Risk", "score": 0.2}
```

# ==========================

# 🏠 HOME ROUTE

# ==========================

@app.route("/")
def home():
return "Aarogya Suchak Running 🚀"

# ==========================

# 🔥 TEST API (IMPORTANT)

# ==========================

@app.route("/api/data")
def get_data():
return jsonify({
"status": "success",
"message": "Backend connected successfully 🎉"
})

# ==========================

# 🔥 MAIN PREDICTION API

# ==========================

@app.route('/predict_all', methods=['POST'])
def predict_all():
try:
data = request.get_json()

```
    diabetes = get_diabetes_result(data)
    heart = get_heart_result(data)
    liver = get_liver_result(data)
    kidney = get_kidney_result(data)

    results = [diabetes, heart, liver, kidney]
    best = max(results, key=lambda x: x["score"])

    return jsonify({
        "disease": best["disease"],
        "risk": best["risk"]
    })

except Exception as e:
    return jsonify({"error": str(e)})
```

# ==========================

# 🔐 AUTH APIs

# ==========================

@app.route("/signup", methods=["POST"])
def signup():
data = request.get_json()
email = data.get("email")
password = data.get("password")

```
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT,
    password TEXT
)
""")

cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
conn.commit()
conn.close()

return jsonify({"status": "success"})
```

@app.route("/login", methods=["POST"])
def login():
data = request.get_json()
email = data.get("email")
password = data.get("password")

```
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
user = cursor.fetchone()
conn.close()

if user:
    return jsonify({"status": "success"})
else:
    return jsonify({"status": "error"})
```

# ==========================

# 🤖 CHATBOT API

# ==========================

@app.route('/chat', methods=['POST'])
def chat():
data = request.get_json()
msg = data.get("message", "").lower()

```
disease = data.get("disease", "")
risk = data.get("risk", "")

if "liver" in msg:
    reply = "Avoid alcohol, eat healthy, consult doctor."
elif "kidney" in msg:
    reply = "Drink water, reduce salt."
elif "heart" in msg:
    reply = "Avoid oily food, exercise."
elif "diabetes" in msg:
    reply = "Control sugar intake."
elif "hi" in msg or "hello" in msg:
    reply = "Hi! I am Aaru, your health assistant."
else:
    reply = f"Based on your result ({disease} - {risk}), take care."

return jsonify({"reply": reply})
```

# ==========================

# 🚀 RUN SERVER

# ==========================

if **name** == "**main**":
app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
