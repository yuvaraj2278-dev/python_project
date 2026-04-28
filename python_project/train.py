import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import pickle

print("--- Starting Training Process ---")

# 1. Load Data
try:
    df = pd.read_csv('online_shoppers_intention.csv')
    print("Dataset loaded successfully.")
except FileNotFoundError:
    print("ERROR: File not found.")
    exit()

# 2. Preprocessing
df = df.dropna()
le = LabelEncoder()
cols_to_encode = ['Month', 'VisitorType', 'Weekend', 'Revenue']

for col in cols_to_encode:
    df[col] = le.fit_transform(df[col])

X = df.drop('Revenue', axis=1)
y = df['Revenue']

# 3. Train Model
print("Training model...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# 4. Save Model
with open('purchase_model.pkl', 'wb') as file:
    pickle.dump(model, file)

print("SUCCESS: 'purchase_model.pkl' created!")