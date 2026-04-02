import pandas as pd

df = pd.read_csv("datasets/raw/heart_disease.csv")

df = df.dropna()

df.rename(columns={
    "sex":"gender",
    "thalach":"bpm"
}, inplace=True)

df.to_csv("datasets/processed/heart_disease_clean.csv", index=False)

print("Heart disease dataset cleaned")