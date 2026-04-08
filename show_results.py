import os
import pickle
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, classification_report

# Helper to load existing functions
from pipeline.feature_pipeline import load_dataset, prepare_features

def show_results():
    print("-" * 50)
    print("AI HEARTBEAT DISEASE PREDICTOR - PERFORMANCE RESULTS")
    print("-" * 50)
    
    # 1. Load Data
    try:
        df = load_dataset()
        X, y = prepare_features(df)
        
        # Consistent test split used during training (random_state=42)
        _, X_test, _, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
    except Exception as e:
        print(f"[ERROR] Loading dataset: {e}")
        return

    # 2. Load Models
    try:
        with open("models/saved_models/scaler.pkl", "rb") as f:
            scaler = pickle.load(f)
        
        with open("models/saved_models/heart_model.pkl", "rb") as f:
            model = pickle.load(f)
    except Exception as e:
        print(f"[ERROR] Loading models: {e}")
        return

    # 3. Predict & Calculate
    X_test_scaled = scaler.transform(X_test)
    y_pred = model.predict(X_test_scaled)
    
    accuracy = accuracy_score(y_test, y_pred)
    f1_macro = f1_score(y_test, y_pred, average='macro')
    f1_weighted = f1_score(y_test, y_pred, average='weighted')

    # 4. Show Results
    print(f"\n[MODEL] Random Forest Classifier")
    print(f"[ACCURACY] {accuracy * 100:.2f}%")
    print(f"[F1-SCORE] Macro Average: {f1_macro:.4f}")
    print(f"[F1-SCORE] Weighted Average: {f1_weighted:.4f}")
    
    print("\n[CLASSIFICATION REPORT]")
    print(classification_report(y_test, y_pred))
    
    print("-" * 50)
    print("NOTE: This system is intended for decision support and not as a replacement for professional medical diagnosis.")
    print("-" * 50)

if __name__ == "__main__":
    show_results()
