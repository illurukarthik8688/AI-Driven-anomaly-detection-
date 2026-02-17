from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)
model = joblib.load("failure_model.pkl")

@app.route("/")
def home():
    return "CICD pipeline hai bhai"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    features = np.array([[
        data["build_time"],
        data["failure_rate"],
        data["commit_freq"],
        data["deploy_delay"]
    ]])

    prediction = model.predict(features)[0]

    return jsonify({
        "prediction": int(prediction),
        "result": "Anomaly" if prediction == 1 else "Normal"
    })

if __name__ == "__main__":
    app.run(debug=True)
