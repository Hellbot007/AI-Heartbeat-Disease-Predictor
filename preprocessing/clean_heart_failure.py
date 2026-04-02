import pandas as pd

df = pd.read_csv("datasets/raw/heart_failure.csv")

df = df.dropna()

df.rename(columns={
    "DEATH_EVENT":"disease_label"
}, inplace=True)

df.to_csv("datasets/processed/heart_failure_clean.csv", index=False)

print("Heart failure dataset cleaned")