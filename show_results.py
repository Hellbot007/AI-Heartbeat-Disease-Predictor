import os
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix, precision_recall_fscore_support

# Helper to load existing functions
from pipeline.feature_pipeline import load_dataset, prepare_features

def show_results():
    print("-" * 50)
    print("AI HEARTBEAT DISEASE PREDICTOR - INDIVIDUAL MODEL PERFORMANCE")
    print("-" * 50)
    
    # 1. Load Data
    try:
        df = load_dataset()
        X, y = prepare_features(df)
        
        # Consistent test split used during training (random_state=42)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
    except Exception as e:
        print(f"[ERROR] Loading dataset: {e}")
        return

    # 2. Impute and Scale Features
    imputer = SimpleImputer(strategy='mean')
    scaler = StandardScaler()
    
    X_train_imputed = imputer.fit_transform(X_train)
    X_test_imputed = imputer.transform(X_test)
    
    X_train_scaled = scaler.fit_transform(X_train_imputed)
    X_test_scaled = scaler.transform(X_test_imputed)

    # 3. Define Models
    models = {
        "Random Forest": RandomForestClassifier(random_state=42),
        "Gradient Boosting": GradientBoostingClassifier(random_state=42),
        "K-Nearest Neighbors": KNeighborsClassifier(),
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42)
    }

    results = []

    # 4. Train & Evaluate Models
    for model_name, model in models.items():
        # Train
        start_time = time.time()
        model.fit(X_train_scaled, y_train)
        train_time = time.time() - start_time
        
        # Train accuracy
        y_train_pred = model.predict(X_train_scaled)
        train_acc = accuracy_score(y_train, y_train_pred)

        # Predict
        y_pred = model.predict(X_test_scaled)
        
        # Metrics
        test_acc = accuracy_score(y_test, y_pred)
        f1_macro = f1_score(y_test, y_pred, average='macro')
        f1_weighted = f1_score(y_test, y_pred, average='weighted')
        
        tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
        
        precision, recall, f1, _ = precision_recall_fscore_support(y_test, y_pred)
        
        results.append({
            "Model": model_name,
            "Train Acc": train_acc,
            "Test Acc": test_acc,
            "F1 Macro": f1_macro,
            "F1 Wt": f1_weighted,
            "TP": tp,
            "TN": tn,
            "FP": fp,
            "FN": fn,
            "Train Time": train_time,
            "P (C0)": precision[0],
            "R (C0)": recall[0],
            "F1 (C0)": f1[0],
            "P (C1)": precision[1],
            "R (C1)": recall[1],
            "F1 (C1)": f1[1]
        })
        
        print(f"\n[MODEL] {model_name}")
        print(f"[TRAIN TIME] {train_time:.4f}s")
        print(f"[TRAIN ACCURACY] {train_acc * 100:.2f}%")
        print(f"[TEST ACCURACY] {test_acc * 100:.2f}%")
        print(f"[F1-SCORE] Macro: {f1_macro:.4f} | Weighted: {f1_weighted:.4f}")
        print(f"[CONFUSION MATRIX] TN: {tn}, FP: {fp}, FN: {fn}, TP: {tp}")

    # Save results to a CSV for updating docx later
    results_df = pd.DataFrame(results)
    results_df.to_csv("tmp/model_results.csv", index=False)

    # 5. Generate Graph
    labels = results_df['Model'].tolist()
    train_acc_vals = results_df['Train Acc'].tolist()
    test_acc_vals = results_df['Test Acc'].tolist()
    f1_macro_vals = results_df['F1 Macro'].tolist()
    
    x = np.arange(len(labels))  # the label locations
    width = 0.25  # the width of the bars

    fig, ax = plt.subplots(figsize=(10, 6))
    rects1 = ax.bar(x - width, train_acc_vals, width, label='Train Acc', color='#4c72b0')
    rects2 = ax.bar(x, test_acc_vals, width, label='Test Acc', color='#dd8452')
    rects3 = ax.bar(x + width, f1_macro_vals, width, label='F1 Macro', color='#55a868')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Score')
    ax.set_title('Training vs Test Accuracy and F1-Score Comparison Across All Four ML Models')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylim([0.0, 1.1])
    ax.legend(loc='lower right')

    fig.tight_layout()
    plt.savefig('model_comparison.png')
    print("\nSaved graph to model_comparison.png")

    print("\n" + "-" * 50)
    print("NOTE: This system is intended for decision support and not as a replacement for professional medical diagnosis.")
    print("-" * 50)

if __name__ == "__main__":
    show_results()
