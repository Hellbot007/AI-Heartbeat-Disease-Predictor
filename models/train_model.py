import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

from pipeline.feature_pipeline import load_dataset, prepare_features
from pipeline.scaler_pipeline import create_scaler


# Load dataset
df = load_dataset()

# Prepare features
X, y = prepare_features(df)

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Scale features
X_train_scaled, X_test_scaled = create_scaler(X_train, X_test)

# Train model
model = RandomForestClassifier(n_estimators=100)

model.fit(X_train_scaled, y_train)

# Accuracy
accuracy = model.score(X_test_scaled, y_test)

print("Model Accuracy:", accuracy)

# Save model
os.makedirs("models/saved_models", exist_ok=True)

with open("models/saved_models/heart_model.pkl", "wb") as f:
    pickle.dump(model, f)