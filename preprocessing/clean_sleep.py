import pandas as pd

df = pd.read_csv("datasets/raw/sleep_health.csv")

df = df.dropna()

df.rename(columns={
    "Heart Rate":"bpm",
    "Stress Level":"stress_level",
    "Physical Activity Level":"activity_level"
}, inplace=True)

df.to_csv("datasets/processed/sleep_clean.csv", index=False)

print("Sleep dataset cleaned")