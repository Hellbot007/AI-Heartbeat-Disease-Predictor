import sys
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

from pipeline.feature_pipeline import load_dataset, prepare_features
from pipeline.scaler_pipeline import create_scaler

# Load dataset
df = load_dataset()
X, y = prepare_features(df)

# Train test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Scale features
X_train_scaled, X_test_scaled = create_scaler(X_train, X_test)

# Train baseline model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

# Evaluate baseline model
y_pred_baseline = model.predict(X_test_scaled)
baseline_accuracy = accuracy_score(y_test, y_pred_baseline)

print(f"Baseline (13 features) Accuracy: {baseline_accuracy:.4f}")

# Feature importances
importances = model.feature_importances_
feature_names = X.columns
feature_importance_df = pd.DataFrame({'feature': feature_names, 'importance': importances})
feature_importance_df = feature_importance_df.sort_values(by='importance', ascending=False)

print("\nFeature Importances:")
print(feature_importance_df)

print("\nEvaluating smaller feature sets:")
# Test top N features
for n in range(12, 1, -1):
    top_n_features = feature_importance_df['feature'].head(n).tolist()
    X_train_sub = X_train[top_n_features]
    X_test_sub = X_test[top_n_features]
    
    # Needs to scale the subset as well
    # Just fit a new scaler on the subset
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    X_train_sub_scaled = scaler.fit_transform(X_train_sub)
    X_test_sub_scaled = scaler.transform(X_test_sub)
    
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train_sub_scaled, y_train)
    score = clf.score(X_test_sub_scaled, y_test)
    print(f"Top {n} features accuracy: {score:.4f} (Features: {', '.join(top_n_features)})")

print("\n" + "-" * 50)
print("NOTE: This system is intended for decision support and not as a replacement for professional medical diagnosis.")
print("-" * 50)
