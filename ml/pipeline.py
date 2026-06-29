"""
Full ML Pipeline Orchestrator.
Runs: preprocessing → model comparison → explainability → save artifacts.
"""
import os
import sys
import time

ML_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ML_DIR)


def run_full_pipeline():
    """Execute the complete ML pipeline."""
    print("=" * 60)
    print("  AI Meal Demand — ML Training Pipeline")
    print("=" * 60)
    start = time.time()

    # Step 1: Preprocessing
    print("\n" + "=" * 60)
    print("  STEP 1: Data Preprocessing")
    print("=" * 60)
    from preprocessing import run_preprocessing
    train, test, feature_cols = run_preprocessing()

    # Step 2: Model Comparison
    print("\n" + "=" * 60)
    print("  STEP 2: Model Training & Comparison")
    print("=" * 60)
    from model_comparison import run_model_comparison
    best_key, best_model = run_model_comparison()

    # Step 3: Explainability
    print("\n" + "=" * 60)
    print("  STEP 3: Explainable AI (SHAP)")
    print("=" * 60)
    from explainability import run_explainability
    importance, explanations = run_explainability()

    elapsed = time.time() - start
    print("\n" + "=" * 60)
    print(f"  ML PIPELINE COMPLETE — Total time: {elapsed:.1f}s")
    print(f"  Best model: {best_key}")
    print(f"  Artifacts: {os.path.join(ML_DIR, 'models')}")
    print("=" * 60)


if __name__ == "__main__":
    run_full_pipeline()
