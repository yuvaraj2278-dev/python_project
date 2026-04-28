import joblib
import pandas as pd

# 1. Load the trained model
model = joblib.load('shopper_model.joblib')
print("✅ Model Loaded.")

# 2. Create a fake "new visitor"
# Let's pretend a new visitor just landed on the site.
# [Administrative, Administrative_Duration, Informational, Informational_Duration, 
#  ProductRelated, ProductRelated_Duration, BounceRates, ExitRates, 
#  PageValues, SpecialDay, Month, OperatingSystems, Browser, Region, TrafficType, VisitorType, Weekend]

# Example: A visitor who spent a lot of time on product pages (PageValues = 50)
new_visitor = pd.DataFrame([[
    0, 0.0, 0, 0.0, 
    25, 500.0, 0.0, 0.02, 
    50.0, 0.0, 'Nov', 1, 1, 1, 1, 'Returning_Visitor', False
]], columns=[
    'Administrative', 'Administrative_Duration', 'Informational', 'Informational_Duration',
    'ProductRelated', 'ProductRelated_Duration', 'BounceRates', 'ExitRates', 
    'PageValues', 'SpecialDay', 'Month', 'OperatingSystems', 'Browser', 
    'Region', 'TrafficType', 'VisitorType', 'Weekend'
])

# 3. Preprocess the new visitor (One-Hot Encoding like before)
# We need to make sure the columns match the training data
new_visitor_encoded = pd.get_dummies(new_visitor, columns=['Month', 'VisitorType'], drop_first=True)

# IMPORTANT: The model expects all columns from training. 
# If a column is missing (e.g., 'Month_June'), we fill it with 0.
# For simplicity in this demo, we manually align columns:
# (In a real app, you would save the list of columns from training)

# Get the columns the model was trained on
trained_columns = model.feature_names_in_

# Reindex the new visitor data to match trained columns, filling missing with 0
new_visitor_encoded = new_visitor_encoded.reindex(columns=trained_columns, fill_value=0)

# 4. Predict
prediction = model.predict(new_visitor_encoded)
probability = model.predict_proba(new_visitor_encoded)

print(f"\n--- Prediction for New Visitor ---")
print(f"Will Purchase? {'YES ✅' if prediction[0] else 'NO ❌'}")
print(f"Confidence: {probability[0][1]*100:.1f}%")