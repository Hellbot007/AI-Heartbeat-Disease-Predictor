import pickle
import numpy as np


def prepare_input(user_data):

    # Load scaler
    with open("models/saved_models/scaler.pkl", "rb") as f:
        scaler = pickle.load(f)

    input_array = np.array(user_data).reshape(1, -1)

    input_scaled = scaler.transform(input_array)

    return input_scaled