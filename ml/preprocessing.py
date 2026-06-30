"""
Data Preprocessing for Meal Demand Prediction.
Loads synthetic CSV data and prepares it for ML training.
"""
import pandas as pd
import numpy as np
from datetime import timedelta
import os
import warnings
warnings.filterwarnings("ignore")

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "data-engineering", "output")
ML_DIR = os.path.dirname(os.path.abspath(__file__))


def load_raw_data() -> dict:
    """Load all CSV files from the data-engineering output."""
    print("Loading raw data...")
    data = {}
    files = ["employees", "meal_transactions", "weather_data",
             "holiday_calendar", "visitors", "company_events",
             "daily_menus", "menu_items"]
    for f in files:
        path = os.path.join(DATA_DIR, f"{f}.csv")
        if os.path.exists(path):
            data[f] = pd.read_csv(path)
            print(f"  {f}: {len(data[f]):,} rows")
        else:
            print(f"  WARNING: {path} not found")
            data[f] = pd.DataFrame()
    return data


def aggregate_daily_demand(data: dict) -> pd.DataFrame:
    """
    Aggregate meal transactions into daily demand counts per location and period.
    This is the target variable for prediction.
    """
    print("Aggregating daily demand...")
    txn = data["meal_transactions"].copy()
    txn["transaction_date"] = pd.to_datetime(txn["transaction_date"])

    # Count meals per (date, location, period)
    demand = txn.groupby(["transaction_date", "location_id", "period"]).agg(
        meal_count=("id", "count"),
        waste_count=("was_wasted", "sum"),
    ).reset_index()

    demand.rename(columns={"transaction_date": "date"}, inplace=True)
    print(f"  Daily demand records: {len(demand):,}")
    return demand


def merge_features(demand: pd.DataFrame, data: dict) -> pd.DataFrame:
    """Merge all feature sources into the demand dataframe."""
    print("Merging features...")
    df = demand.copy()

    # --- Date features ---
    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["day"] = df["date"].dt.day
    df["day_of_week"] = df["date"].dt.dayofweek
    df["day_of_year"] = df["date"].dt.dayofyear
    df["week_of_year"] = df["date"].dt.isocalendar().week.astype(int)
    df["quarter"] = df["date"].dt.quarter
    df["is_weekend"] = df["day_of_week"].isin([4, 5]).astype(int)  # Fri=4, Sat=5

    # Egypt work week mapping
    df["egypt_dow"] = (df["day_of_week"] + 2) % 7

    # --- Holiday features ---
    holidays = data["holiday_calendar"].copy()
    if len(holidays) > 0:
        holidays["holiday_date"] = pd.to_datetime(holidays["holiday_date"])
        holiday_dates = set(holidays["holiday_date"].dt.date)
        df["is_holiday"] = df["date"].dt.date.isin(holiday_dates).astype(int)

        # Days to next holiday
        sorted_holidays = sorted(holiday_dates)
        def days_to_next_holiday(d):
            d = d.date() if hasattr(d, 'date') else d
            for h in sorted_holidays:
                if h >= d:
                    return (h - d).days
            return 30
        df["days_to_holiday"] = df["date"].apply(days_to_next_holiday)
        df["days_to_holiday"] = df["days_to_holiday"].clip(0, 30)
    else:
        df["is_holiday"] = 0
        df["days_to_holiday"] = 30

    # --- Weather features ---
    weather = data["weather_data"].copy()
    if len(weather) > 0:
        weather["weather_date"] = pd.to_datetime(weather["weather_date"])
        weather_cols = ["location_id", "weather_date", "temperature_avg",
                        "temperature_high", "humidity_percent", "condition",
                        "wind_speed_kmh", "precipitation_mm"]
        weather = weather[weather_cols].rename(columns={"weather_date": "date"})

        # Encode weather condition
        weather_map = {"sunny": 0, "cloudy": 1, "foggy": 2, "windy": 3,
                       "rainy": 4, "stormy": 5, "snowy": 6}
        weather["weather_code"] = weather["condition"].map(weather_map).fillna(0)
        weather.drop(columns=["condition"], inplace=True)

        df = df.merge(weather, on=["location_id", "date"], how="left")
    else:
        df["temperature_avg"] = 30
        df["humidity_percent"] = 40
        df["weather_code"] = 0

    # --- Location features ---
    locations_info = {
        i + 1: {"type": loc[2], "capacity": loc[4]}
        for i, loc in enumerate([
            ("Headquarters", "HQ-CAI", "office", "Cairo", 2000),
            ("Alexandria Office", "OFF-ALX", "office", "Alexandria", 800),
            ("Suez Office", "OFF-SUZ", "office", "Suez", 600),
            ("6th October Office", "OFF-OCT", "office", "6th October City", 400),
            ("Ain Sokhna Industrial", "IND-ASK", "industrial", "Ain Sokhna", 1500),
            ("Borg El-Arab Plant", "IND-BRG", "industrial", "Borg El-Arab", 1200),
            ("El-Hamra Refinery", "IND-HMR", "industrial", "El-Alamein", 1800),
            ("Abu Qir Processing", "IND-ABQ", "industrial", "Abu Qir", 1000),
            ("Ras Gharib Field", "FLD-RSG", "field", "Ras Gharib", 600),
            ("Gulf of Suez Platform", "FLD-GOS", "field", "Gulf of Suez", 500),
            ("Western Desert Field", "FLD-WDS", "field", "Western Desert", 400),
            ("Belayim Platform", "FLD-BLY", "field", "Belayim", 450),
            ("Assiut Refinery", "IND-AST", "industrial", "Assiut", 350),
            ("El-Mex Industrial", "IND-MEX", "industrial", "El-Mex", 900),
            ("New Administrative Capital", "OFF-NAC", "office", "New Capital", 300),
        ])
    }
    loc_type_map = {"office": 0, "industrial": 1, "field": 2}
    df["location_type"] = df["location_id"].map(lambda x: loc_type_map.get(locations_info.get(x, {}).get("type", "office"), 0))
    df["location_capacity"] = df["location_id"].map(lambda x: locations_info.get(x, {}).get("capacity", 500))

    # --- Visitor features ---
    visitors = data["visitors"].copy()
    if len(visitors) > 0:
        visitors["visit_date"] = pd.to_datetime(visitors["visit_date"])
        visitor_daily = visitors.groupby(["visit_date", "location_id"]).agg(
            visitor_count=("visitor_count", "sum")
        ).reset_index().rename(columns={"visit_date": "date"})
        df = df.merge(visitor_daily, on=["location_id", "date"], how="left")
        df["visitor_count"] = df["visitor_count"].fillna(0)
    else:
        df["visitor_count"] = 0

    # --- Event features ---
    events = data["company_events"].copy()
    if len(events) > 0:
        events["event_date"] = pd.to_datetime(events["event_date"])
        event_daily = events.groupby(["event_date", "location_id"]).agg(
            has_event=("id", "count"),
            event_attendees=("expected_attendees", "sum"),
        ).reset_index().rename(columns={"event_date": "date"})
        event_daily["has_event"] = (event_daily["has_event"] > 0).astype(int)
        df = df.merge(event_daily, on=["location_id", "date"], how="left")
        df["has_event"] = df["has_event"].fillna(0).astype(int)
        df["event_attendees"] = df["event_attendees"].fillna(0)
    else:
        df["has_event"] = 0
        df["event_attendees"] = 0

    # --- Employee count per location ---
    employees = data["employees"].copy()
    if len(employees) > 0:
        active_count = employees[employees["is_active"] == True].groupby("work_location_id").size()
        df["active_employees"] = df["location_id"].map(active_count).fillna(0)
    else:
        df["active_employees"] = 100

    # --- Period encoding ---
    period_map = {"breakfast": 0, "lunch": 1, "dinner": 2}
    df["period_code"] = df["period"].map(period_map)

    # --- Menu diversity (count of unique meal items on that day/location) ---
    menus = data["daily_menus"].copy()
    items = data["menu_items"].copy()
    if len(menus) > 0 and len(items) > 0:
        menus["menu_date"] = pd.to_datetime(menus["menu_date"])
        menu_diversity = items.groupby("menu_id").agg(
            item_count=("meal_type_id", "nunique")
        ).reset_index()
        menu_with_date = menus.merge(menu_diversity, left_on="id", right_on="menu_id", how="left")
        menu_with_date = menu_with_date[["menu_date", "location_id", "item_count"]].rename(
            columns={"menu_date": "date"})
        df = df.merge(menu_with_date, on=["location_id", "date"], how="left")
        df["menu_item_count"] = df["item_count"].fillna(7)
        df.drop(columns=["item_count"], inplace=True, errors="ignore")
    else:
        df["menu_item_count"] = 7

    # Fill remaining NAs
    df = df.fillna(0)

    print(f"  Final feature matrix: {df.shape}")
    return df


def add_lag_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add time-series lag and rolling features."""
    print("Adding lag features...")
    df = df.sort_values(["location_id", "period", "date"]).reset_index(drop=True)

    group_cols = ["location_id", "period"]

    for lag in [1, 2, 3, 7, 14, 28]:
        df[f"lag_{lag}d"] = df.groupby(group_cols)["meal_count"].shift(lag)

    # Rolling statistics
    for window in [7, 14, 30]:
        rolling = df.groupby(group_cols)["meal_count"].transform(
            lambda x: x.shift(1).rolling(window, min_periods=1).mean()
        )
        df[f"rolling_mean_{window}d"] = rolling

        rolling_std = df.groupby(group_cols)["meal_count"].transform(
            lambda x: x.shift(1).rolling(window, min_periods=1).std()
        )
        df[f"rolling_std_{window}d"] = rolling_std

    # Expanding mean (historical average)
    df["expanding_mean"] = df.groupby(group_cols)["meal_count"].transform(
        lambda x: x.shift(1).expanding(min_periods=1).mean()
    )

    # Same day of week last week
    df["same_dow_last_week"] = df.groupby(group_cols)["meal_count"].shift(7)

    # Fill NAs from lags with expanding mean or 0
    lag_cols = [c for c in df.columns if c.startswith(("lag_", "rolling_", "expanding_", "same_"))]
    df[lag_cols] = df[lag_cols].fillna(0)

    print(f"  Added {len(lag_cols)} lag/rolling features")
    return df


def prepare_train_test(df: pd.DataFrame, test_days: int = 30):
    """Split into train/test using time-based split."""
    print(f"Splitting train/test (last {test_days} days for test)...")
    df = df.sort_values("date").reset_index(drop=True)

    max_date = df["date"].max()
    split_date = max_date - timedelta(days=test_days)

    train = df[df["date"] <= split_date].copy()
    test = df[df["date"] > split_date].copy()

    # Drop rows with too many NaN lags (first 30 days)
    min_date = df["date"].min() + timedelta(days=30)
    train = train[train["date"] >= min_date]

    print(f"  Train: {len(train):,} rows ({train['date'].min()} to {train['date'].max()})")
    print(f"  Test:  {len(test):,} rows ({test['date'].min()} to {test['date'].max()})")

    # Define feature columns (exclude target, identifiers, date)
    exclude = ["id", "date", "meal_count", "waste_count", "period"]
    feature_cols = [c for c in df.columns if c not in exclude]

    return train, test, feature_cols


def run_preprocessing():
    """Execute full preprocessing pipeline."""
    data = load_raw_data()
    demand = aggregate_daily_demand(data)
    df = merge_features(demand, data)
    df = add_lag_features(df)
    train, test, feature_cols = prepare_train_test(df)

    # Save processed data
    os.makedirs(os.path.join(ML_DIR, "processed"), exist_ok=True)
    train.to_csv(os.path.join(ML_DIR, "processed", "train.csv"), index=False)
    test.to_csv(os.path.join(ML_DIR, "processed", "test.csv"), index=False)

    with open(os.path.join(ML_DIR, "processed", "feature_cols.txt"), "w") as f:
        f.write("\n".join(feature_cols))

    print(f"\nSaved processed data to {os.path.join(ML_DIR, 'processed')}")
    print(f"Feature columns ({len(feature_cols)}): {feature_cols[:10]}...")
    return train, test, feature_cols


if __name__ == "__main__":
    run_preprocessing()
