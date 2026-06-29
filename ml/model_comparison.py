"""
Model Comparison — Train & evaluate multiple ML algorithms.
Compares XGBoost, LightGBM, CatBoost, Random Forest, Gradient Boosting.
"""
import os
import json
import time
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import warnings
warnings.filterwarnings("ignore")

ML_DIR = os.path.dirname(os.path.abspath(__file__))


def mean_absolute_percentage_error(y_true, y_pred):
    """MAPE metric, handling zeros."""
    mask = y_true != 0
    if mask.sum() == 0:
        return 0.0
    return np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100


def load_processed_data():
    """Load preprocessed train/test data."""
    proc_dir = os.path.join(ML_DIR, "processed")
    train = pd.read_csv(os.path.join(proc_dir, "train.csv"))
    test = pd.read_csv(os.path.join(proc_dir, "test.csv"))
    with open(os.path.join(proc_dir, "feature_cols.txt")) as f:
        feature_cols = [line.strip() for line in f if line.strip()]
    return train, test, feature_cols


def evaluate_model(y_true, y_pred, name="Model"):
    """Compute and print evaluation metrics."""
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mape = mean_absolute_percentage_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    print(f"  {name:25s} | MAE: {mae:8.2f} | RMSE: {rmse:8.2f} | MAPE: {mape:6.2f}% | R²: {r2:.4f}")
    return {"name": name, "mae": mae, "rmse": rmse, "mape": mape, "r2": r2}


def train_models(train, test, feature_cols):
    """Train all candidate models and compare."""
    X_train = train[feature_cols].values
    y_train = train["meal_count"].values
    X_test = test[feature_cols].values
    y_test = test["meal_count"].values

    print(f"\nTraining on {len(X_train):,} samples, testing on {len(X_test):,} samples")
    print(f"Features: {len(feature_cols)}")
    print("-" * 85)

    results = []
    models = {}

    # 1. Random Forest
    print("\n[1/5] Random Forest...")
    t0 = time.time()
    rf = RandomForestRegressor(n_estimators=200, max_depth=15, min_samples_leaf=10,
                                n_jobs=-1, random_state=42)
    rf.fit(X_train, y_train)
    rf_pred = rf.predict(X_test)
    rf_time = time.time() - t0
    res = evaluate_model(y_test, rf_pred, "Random Forest")
    res["time"] = rf_time
    results.append(res)
    models["random_forest"] = rf

    # 2. Gradient Boosting
    print("\n[2/5] Gradient Boosting...")
    t0 = time.time()
    gb = GradientBoostingRegressor(n_estimators=300, max_depth=6, learning_rate=0.1,
                                    subsample=0.8, random_state=42)
    gb.fit(X_train, y_train)
    gb_pred = gb.predict(X_test)
    gb_time = time.time() - t0
    res = evaluate_model(y_test, gb_pred, "Gradient Boosting")
    res["time"] = gb_time
    results.append(res)
    models["gradient_boosting"] = gb

    # 3. XGBoost
    try:
        import xgboost as xgb
        print("\n[3/5] XGBoost...")
        t0 = time.time()
        xgb_model = xgb.XGBRegressor(
            n_estimators=500, max_depth=7, learning_rate=0.05,
            subsample=0.8, colsample_bytree=0.8, reg_alpha=0.1, reg_lambda=1.0,
            n_jobs=-1, random_state=42, verbosity=0
        )
        xgb_model.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=False)
        xgb_pred = xgb_model.predict(X_test)
        xgb_time = time.time() - t0
        res = evaluate_model(y_test, xgb_pred, "XGBoost")
        res["time"] = xgb_time
        results.append(res)
        models["xgboost"] = xgb_model
    except ImportError:
        print("  XGBoost not installed, skipping...")

    # 4. LightGBM
    try:
        import lightgbm as lgb
        print("\n[4/5] LightGBM...")
        t0 = time.time()
        lgb_model = lgb.LGBMRegressor(
            n_estimators=500, max_depth=7, learning_rate=0.05,
            subsample=0.8, colsample_bytree=0.8, reg_alpha=0.1, reg_lambda=1.0,
            n_jobs=-1, random_state=42, verbose=-1
        )
        lgb_model.fit(X_train, y_train, eval_set=[(X_test, y_test)])
        lgb_pred = lgb_model.predict(X_test)
        lgb_time = time.time() - t0
        res = evaluate_model(y_test, lgb_pred, "LightGBM")
        res["time"] = lgb_time
        results.append(res)
        models["lightgbm"] = lgb_model
    except ImportError:
        print("  LightGBM not installed, skipping...")

    # 5. CatBoost
    try:
        from catboost import CatBoostRegressor
        print("\n[5/5] CatBoost...")
        t0 = time.time()
        cb_model = CatBoostRegressor(
            iterations=500, depth=7, learning_rate=0.05,
            l2_leaf_reg=3, random_seed=42, verbose=0
        )
        cb_model.fit(X_train, y_train, eval_set=(X_test, y_test))
        cb_pred = cb_model.predict(X_test)
        cb_time = time.time() - t0
        res = evaluate_model(y_test, cb_pred, "CatBoost")
        res["time"] = cb_time
        results.append(res)
        models["catboost"] = cb_model
    except ImportError:
        print("  CatBoost not installed, skipping...")

    return results, models


def select_best_model(results, models, feature_cols):
    """Select and save the best model based on R² score."""
    print("\n" + "=" * 85)
    print("MODEL COMPARISON RESULTS")
    print("=" * 85)

    results_df = pd.DataFrame(results).sort_values("r2", ascending=False)
    print(results_df.to_string(index=False))

    best = results_df.iloc[0]
    best_name = best["name"]
    best_key = best_name.lower().replace(" ", "_")

    print(f"\nBest Model: {best_name} (R2={best['r2']:.4f}, MAE={best['mae']:.2f})")

    # Save best model
    os.makedirs(os.path.join(ML_DIR, "models"), exist_ok=True)
    model_path = os.path.join(ML_DIR, "models", "best_model.joblib")
    joblib.dump(models[best_key], model_path)
    print(f"  Saved to {model_path}")

    # Save metadata
    meta = {
        "model_name": best_name,
        "algorithm": best_key,
        "mae": float(best["mae"]),
        "rmse": float(best["rmse"]),
        "mape": float(best["mape"]),
        "r2": float(best["r2"]),
        "feature_count": len(feature_cols),
        "feature_names": feature_cols,
        "all_results": results,
    }
    meta_path = os.path.join(ML_DIR, "models", "model_metadata.json")
    with open(meta_path, "w") as f:
        json.dump(meta, f, indent=2, default=str)

    # Save comparison CSV
    results_df.to_csv(os.path.join(ML_DIR, "reports", "model_comparison.csv"), index=False)
    return best_key, models[best_key]


def run_model_comparison():
    """Execute full model comparison pipeline."""
    os.makedirs(os.path.join(ML_DIR, "reports"), exist_ok=True)
    train, test, feature_cols = load_processed_data()
    results, models = train_models(train, test, feature_cols)
    best_key, best_model = select_best_model(results, models, feature_cols)
    return best_key, best_model


if __name__ == "__main__":
    run_model_comparison()
