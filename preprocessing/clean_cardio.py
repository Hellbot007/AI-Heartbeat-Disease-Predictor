import pandas as pd

df = pd.read_csv("datasets/raw/cardio_train.csv")

df = df.dropna()

df.rename(columns={
    "cardio":"disease_label",
    "ap_hi":"blood_pressure_high",
    "ap_lo":"blood_pressure_low"
}, inplace=True)

df.to_csv("datasets/processed/cardio_clean.csv", index=False)

print("Cardio dataset cleaned")