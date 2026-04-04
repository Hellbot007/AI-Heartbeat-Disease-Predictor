import pandas as pd


def load_dataset():

    path = "datasets/final/heart_combined_dataset.csv"

    df = pd.read_csv(path, low_memory=False)

    return df


def prepare_features(df):

    print("Dataset Columns:", df.columns)

    target = "num"

    if target not in df.columns:
        raise Exception("Target column 'num' not found")

    features_list = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalch', 'exang', 'oldpeak', 'slope', 'ca', 'thal']

    # Make sure we only use the numeric columns that correspond to the frontend
    df = df[features_list + [target]].copy()
    
    # Convert all columns to numeric, coercing errors to NaN
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Fill missing values
    df = df.fillna(df.mean())

    # Separate features and label
    X = df.drop(columns=[target])

    # Convert to binary classification
    y = df[target].apply(lambda x: 0 if x == 0 else 1)

    return X, y