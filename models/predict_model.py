import pickle
import numpy as np

model = pickle.load(open("backend/models/saved_models/heart_model.pkl","rb"))
scaler = pickle.load(open("backend/models/saved_models/scaler.pkl","rb"))

def predict_heart_risk(features):

    features = np.array(features).reshape(1,-1)
    features_scaled = scaler.transform(features)

    prediction = model.predict(features_scaled)

    return prediction