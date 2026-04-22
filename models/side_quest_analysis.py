import sys
import os
import pandas as pd
import numpy as np
import time
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, f1_score, classification_report
from sklearn.preprocessing import StandardScaler

# Add parent directory to path to import local modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from pipeline.feature_pipeline import load_dataset, prepare_features
except ImportError:
    print("[ERROR] Could not import pipeline modules. Make sure you are running from the project root.")
    sys.exit(1)

def run_analysis():
    print("=" * 60)
    print("      SIDE QUEST: NUMERICAL MODEL COMPARISON ANALYSIS")
    print("=" * 60)
    
    # 1. Load and Prepare Data
    try:
        # Load raw dataset
        df = load_dataset()
        
        # Prepare features using the existing pipeline
        # (This handles numeric conversion and initial mean fill)
        X, y = prepare_features(df)
        
        # Fill any remaining NaNs (e.g. from columns that were entirely missing) with 0
        X = X.fillna(0)

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        
        # Scale data
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        print(f"Dataset loaded: {len(df)} samples, {X.shape[1]} features.")
    except Exception as e:
        print(f"[ERROR] Failed to load data: {e}")
        import traceback
        traceback.print_exc()
        return


    # 2. Define Models
    models = {
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
        "Gradient Boosting": GradientBoostingClassifier(random_state=42),
        "SVM (RBF Kernel)": SVC(probability=True, random_state=42),
        "K-Nearest Neighbors": KNeighborsClassifier(n_neighbors=5),
        "Decision Tree": DecisionTreeClassifier(random_state=42)
    }

    # 3. Train and Evaluate
    print("\n[2/4] Training and evaluating models individually...")
    results = []
    
    # Header for progress
    print(f"{'Model Name':<25} | {'Accuracy':<10} | {'F1-Macro':<10} | {'Training Time':<15}")
    print("-" * 65)

    for name, clf in models.items():
        start_time = time.time()
        clf.fit(X_train_scaled, y_train)
        end_time = time.time()
        
        y_pred = clf.predict(X_test_scaled)
        
        acc = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average='macro')
        train_time = end_time - start_time
        
        results.append({
            "Model": name,
            "Accuracy": acc,
            "F1-Macro": f1,
            "Time": train_time
        })
        
        print(f"{name:<25} | {acc:>8.2%} | {f1:>8.4f} | {train_time:>8.4f}s")

    # 4. Final Comparison Report
    print("\n[3/4] Generating detailed report...")
    results_df = pd.DataFrame(results).sort_values(by="Accuracy", ascending=False)
    
    print("\nRANKED BY ACCURACY:")
    print(results_df.to_string(index=False))
    
    best_model = results_df.iloc[0]
    print(f"\nWINNER: {best_model['Model']} with {best_model['Accuracy']:.2%} accuracy!")

    print("\n" + "=" * 60)
    print("NOTE: This analysis is for numerical comparison only.")
    print("It does NOT affect the main 'heart_model.pkl' used in the app.")
    print("=" * 60)

if __name__ == "__main__":
    run_analysis()
