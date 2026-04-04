import pickle
import numpy as np
import os

model_path = os.path.join(os.path.dirname(__file__), "saved_models", "heart_model.pkl")
scaler_path = os.path.join(os.path.dirname(__file__), "saved_models", "scaler.pkl")

model = pickle.load(open(model_path, "rb"))
scaler = pickle.load(open(scaler_path, "rb"))

def predict_heart_risk(features):

    imputed_features = []
    for i, val in enumerate(features):
        if val is None:
            imputed_features.append(scaler.mean_[i])
        else:
            imputed_features.append(val)

    features_array = np.array(imputed_features).reshape(1,-1)
    features_scaled = scaler.transform(features_array)

    prediction = model.predict(features_scaled)

    return int(prediction[0])