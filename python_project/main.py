from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import joblib

# 1. Initialize App
app = FastAPI()

# 2. Enable CORS (CRITICAL: Allows HTML to talk to Python)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Load Model
model = joblib.load('shopper_model.joblib')

# 4. Define Prediction Endpoint
@app.post("/predict")
def predict(data: dict):
    # Create DataFrame from input
    df_input = pd.DataFrame([data])
    
    # Preprocess (One-Hot Encoding)
    df_encoded = pd.get_dummies(df_input, columns=['Month', 'VisitorType'], drop_first=True)
    
    # Align columns
    trained_columns = model.feature_names_in_
    df_encoded = df_encoded.reindex(columns=trained_columns, fill_value=0)
    
    # Predict
    prediction = model.predict(df_encoded)
    probability = model.predict_proba(df_encoded)
    
    return {
        "prediction": bool(prediction[0]),
        "confidence": float(probability[0][1])
    }