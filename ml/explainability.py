"""
Explainable AI — SHAP-based model explanations.
Generates feature importance and natural language explanations.
"""
import os
import json
import joblib
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

ML_DIR = os.path.dirname(os.path.abspath(__file__))


def load_model_and_data():
    """Load the best model and test data."""
    model = joblib.load(os.path.join(ML_DIR, "models", "best_model.joblib"))
    test = pd.read_csv(os.path.join(ML_DIR, "processed", "test.csv"))
    with open(os.path.join(ML_DIR, "processed", "feature_cols.txt")) as f:
        feature_cols = [line.strip() for line in f if line.strip()]
    with open(os.path.join(ML_DIR, "models", "model_metadata.json")) as f:
        metadata = json.load(f)
    return model, test, feature_cols, metadata


def compute_shap_values(model, X, feature_cols, max_samples=1000):
    """Compute SHAP values for the model."""
    try:
        import shap
        print("Computing SHAP values...")
        # Subsample for speed
        if len(X) > max_samples:
            idx = np.random.choice(len(X), max_samples, replace=False)
            X_sample = X[idx]
        else:
            X_sample = X

        # Use TreeExplainer for tree-based models
        try:
            explainer = shap.TreeExplainer(model)
            shap_values = explainer.shap_values(X_sample)
        except Exception:
            explainer = shap.Explainer(model, X_sample)
            shap_values = explainer(X_sample).values

        # Mean absolute SHAP per feature
        mean_abs_shap = np.abs(shap_values).mean(axis=0)
        importance = pd.DataFrame({
            "feature": feature_cols,
            "mean_abs_shap": mean_abs_shap,
        }).sort_values("mean_abs_shap", ascending=False)

        print(f"  Top 10 features by SHAP importance:")
        for _, row in importance.head(10).iterrows():
            print(f"    {row['feature']:30s} {row['mean_abs_shap']:.4f}")

        return shap_values, importance, explainer

    except ImportError:
        print("  SHAP not installed. Using built-in feature importance...")
        return compute_builtin_importance(model, feature_cols)


def compute_builtin_importance(model, feature_cols):
    """Fallback: use model's built-in feature importance."""
    try:
        importances = model.feature_importances_
    except AttributeError:
        importances = np.ones(len(feature_cols)) / len(feature_cols)

    importance = pd.DataFrame({
        "feature": feature_cols,
        "importance": importances,
    }).sort_values("importance", ascending=False)

    print(f"  Top 10 features by built-in importance:")
    for _, row in importance.head(10).iterrows():
        print(f"    {row['feature']:30s} {row['importance']:.4f}")

    return None, importance, None


def generate_explanation(feature_values: dict, shap_contributions: dict,
                         prediction: float) -> str:
    """Generate a natural language explanation for a single prediction."""
    # Human-readable feature names
    feature_labels = {
        "lag_1d": "yesterday's demand",
        "lag_7d": "same day last week",
        "rolling_mean_7d": "7-day average demand",
        "rolling_mean_30d": "30-day average demand",
        "day_of_week": "day of the week",
        "saudi_dow": "Saudi work day",
        "is_weekend": "weekend status",
        "is_holiday": "holiday status",
        "days_to_holiday": "proximity to holiday",
        "temperature_avg": "temperature",
        "temperature_high": "high temperature",
        "humidity_percent": "humidity",
        "weather_code": "weather condition",
        "location_type": "location type",
        "location_capacity": "facility capacity",
        "active_employees": "active employee count",
        "visitor_count": "expected visitors",
        "has_event": "company event",
        "event_attendees": "event attendance",
        "menu_item_count": "menu variety",
        "month": "time of year",
        "quarter": "quarter",
        "period_code": "meal period",
    }

    # Sort contributions by absolute value
    sorted_contribs = sorted(shap_contributions.items(), key=lambda x: abs(x[1]), reverse=True)
    top_factors = sorted_contribs[:5]

    parts = []
    for feat, contrib in top_factors:
        label = feature_labels.get(feat, feat.replace("_", " "))
        val = feature_values.get(feat, "")
        direction = "increased" if contrib > 0 else "decreased"
        parts.append(f"{label} ({val}) {direction} the prediction by {abs(contrib):.1f}")

    explanation = f"The predicted meal count is {prediction:.0f}. "
    if parts:
        explanation += "Key factors: " + "; ".join(parts) + "."

    return explanation


def explain_predictions(model, test, feature_cols, n_samples=5):
    """Generate explanations for sample predictions."""
    X_test = test[feature_cols].values
    shap_values, importance, explainer = compute_shap_values(model, X_test, feature_cols)

    # Save feature importance
    os.makedirs(os.path.join(ML_DIR, "reports"), exist_ok=True)
    importance.to_csv(os.path.join(ML_DIR, "reports", "feature_importance.csv"), index=False)

    # Generate sample explanations
    explanations = []
    predictions = model.predict(X_test[:n_samples])

    for i in range(min(n_samples, len(X_test))):
        feature_values = {col: test[col].iloc[i] for col in feature_cols}

        if shap_values is not None:
            contribs = {col: float(shap_values[i, j]) for j, col in enumerate(feature_cols)}
        else:
            contribs = {col: float(importance.loc[importance["feature"] == col, "importance"].values[0])
                        for col in feature_cols if col in importance["feature"].values}

        explanation = generate_explanation(feature_values, contribs, predictions[i])
        explanations.append({
            "date": str(test["date"].iloc[i]),
            "location_id": int(test["location_id"].iloc[i]),
            "period": test["period"].iloc[i],
            "predicted": float(predictions[i]),
            "actual": float(test["meal_count"].iloc[i]),
            "explanation": explanation,
        })
        print(f"\n  Sample {i + 1}: {explanation}")

    # Save explanations
    with open(os.path.join(ML_DIR, "reports", "sample_explanations.json"), "w") as f:
        json.dump(explanations, f, indent=2, default=str)

    return importance, explanations


def run_explainability():
    """Execute explainability pipeline."""
    model, test, feature_cols, metadata = load_model_and_data()
    importance, explanations = explain_predictions(model, test, feature_cols)
    return importance, explanations


if __name__ == "__main__":
    run_explainability()
