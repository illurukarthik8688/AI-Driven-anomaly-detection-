import joblib
import numpy as np
import sys

model = joblib.load("failure_model.pkl")
encoders = joblib.load("encoders.pkl")
target_encoder = joblib.load("target_encoder.pkl")

# Example pipeline s tage (hardcoded for now)
new_data = {
    "stage_name": "Deploy",
    "job_name": "deploy_to_dev",
    "task_name": "deploy",
    "pipeline_id": "pipe-acoca"
}

encoded_input = []

for col in ["stage_name", "job_name", "task_name", "pipeline_id"]:
    encoded_input.append(encoders[col].transform([new_data[col]])[0])

encoded_input = np.array([encoded_input])

prediction = model.predict(encoded_input)[0]
confidence = max(model.predict_proba(encoded_input)[0])
predicted_status = target_encoder.inverse_transform([prediction])[0]

print(f"Prediction: {predicted_status}")
print(f"Confidence: {confidence*100:.2f}%")

# If high risk, fail pipeline
if predicted_status.lower() == "failed" and confidence > 0.6:
    print("⚠️ High failure risk detected. Stopping pipeline.")
    sys.exit(1)
else:
    print("✅ Safe to continue pipeline.")
