import pandas as pd

d1 = pd.read_csv("datasets/processed/heart_disease_clean.csv")
d2 = pd.read_csv("datasets/processed/heart_failure_clean.csv")
d3 = pd.read_csv("datasets/processed/cardio_clean.csv")
d4 = pd.read_csv("datasets/processed/sleep_clean.csv")

combined = pd.concat([d1,d2,d3,d4], ignore_index=True)

combined.to_csv("datasets/final/heart_combined_dataset.csv", index=False)

print("Datasets merged successfully")