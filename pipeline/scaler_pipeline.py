from sklearn.preprocessing import StandardScaler
import pickle

def create_scaler(X_train, X_test):

    scaler = StandardScaler()

    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # save scaler
    with open("models/saved_models/scaler.pkl", "wb") as f:
        pickle.dump(scaler, f)

    return X_train_scaled, X_test_scaled