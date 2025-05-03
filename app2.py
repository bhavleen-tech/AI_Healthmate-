import pickle
import numpy as np
from flask import Flask, request, jsonify, render_template
import pandas as pd
# Initialize Flask app
app = Flask(__name__)

# Load your trained model from the .pkl file
with open("disease_prediction_model.pkl", "rb") as file:
    model = pickle.load(file)

# Load the disease encoder - add this line
with open("disease_encoder.pkl", "rb") as file:
    disease_encoder = pickle.load(file)

# Define a route for homepage
@app.route("/",methods=["GET"])
def home():
    return render_template("index.html")  # HTML frontend

# Define an API route for predictions
@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get input data from request
        data = request.json  # Get the entire JSON data
        print("Received JSON:", data)  # Debugging log
        
        if not data or "features" not in data:
            return jsonify({"error": "Invalid input data - 'features' key missing"}), 400
        
        # Convert input data to NumPy array
        input_features = np.array(data["features"]).reshape(1, -1)
        
        # If feature_names_in_ exists, use it; otherwise, define manually
        if hasattr(model, "feature_names_in_"):
            new_patient_df = pd.DataFrame(input_features, columns=model.feature_names_in_)
        else:
            feature_names = ["Fever","Cough","Fatigue","Difficulty Breathing","Age","Gender","Blood Pressure","Cholesterol Level"]  # Define manually if needed
            new_patient_df = pd.DataFrame(input_features, columns=feature_names)
        
        print("Processed DataFrame:\n", new_patient_df)  # Debugging log
        
        # Make a prediction
        numeric_prediction = model.predict(new_patient_df)[0]  # Get first element from array
        
        # Convert numeric prediction to disease name using the encoder
        disease_name = disease_encoder.inverse_transform([numeric_prediction])[0]
            
        print(f"Prediction: {numeric_prediction} -> {disease_name}")  # Debugging log
        
        # Return both numeric prediction and disease name
        return jsonify({
            "prediction": int(numeric_prediction),
            "disease": disease_name
        })
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500

# Run Flask app
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=2000, debug=True)