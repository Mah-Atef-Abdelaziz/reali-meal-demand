"""Weather data generator — daily weather per location for 2 years."""
import numpy as np
import pandas as pd
from datetime import timedelta
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import (
    LOCATIONS, WEATHER_PROFILES, START_DATE, END_DATE,
    RANDOM_SEED, OUTPUT_DIR
)

np.random.seed(RANDOM_SEED)


def generate_weather() -> pd.DataFrame:
    """Generate daily weather data for each location."""
    print("Generating weather data...")

    days = (END_DATE - START_DATE).days + 1
    dates = [START_DATE + timedelta(days=d) for d in range(days)]
    rows = []
    row_id = 1

    for loc_idx, (name, code, ltype, city, cap) in enumerate(LOCATIONS, 1):
        profile = WEATHER_PROFILES.get(city, WEATHER_PROFILES["Riyadh"])

        for d in dates:
            # Seasonal temperature interpolation
            month = d.month
            # Summer peak in July (month 7), winter low in January (month 1)
            season_factor = np.sin((month - 1) / 12 * 2 * np.pi - np.pi / 2) * 0.5 + 0.5

            high_base = profile["winter_high"] + (profile["summer_high"] - profile["winter_high"]) * season_factor
            low_base = profile["winter_low"] + (profile["summer_low"] - profile["winter_low"]) * season_factor

            # Add daily noise
            temp_high = round(high_base + np.random.normal(0, 2), 1)
            temp_low = round(low_base + np.random.normal(0, 2), 1)
            temp_avg = round((temp_high + temp_low) / 2, 1)
            humidity = int(np.clip(np.random.normal(45 - season_factor * 20, 10), 10, 95))

            # Weather condition
            rain_prob = profile["rain_prob"] * (1 + (1 - season_factor))  # More rain in winter
            rand = np.random.random()
            if rand < rain_prob * 0.3:
                condition = "stormy"
            elif rand < rain_prob:
                condition = "rainy"
            elif rand < rain_prob + 0.05:
                condition = "foggy"
            elif rand < rain_prob + 0.10:
                condition = "windy"
            elif rand < rain_prob + 0.30:
                condition = "cloudy"
            else:
                condition = "sunny"

            wind = round(np.clip(np.random.exponential(12), 2, 60), 1)
            precip = round(np.random.exponential(2), 1) if condition in ("rainy", "stormy") else 0.0

            rows.append({
                "id": row_id,
                "location_id": loc_idx,
                "weather_date": d.strftime("%Y-%m-%d"),
                "temperature_high": temp_high,
                "temperature_low": temp_low,
                "temperature_avg": temp_avg,
                "humidity_percent": humidity,
                "condition": condition,
                "wind_speed_kmh": wind,
                "precipitation_mm": precip,
            })
            row_id += 1

    df = pd.DataFrame(rows)
    output_path = os.path.join(OUTPUT_DIR, "weather_data.csv")
    df.to_csv(output_path, index=False)
    print(f"  Saved {len(df):,} weather records to {output_path}")
    return df


if __name__ == "__main__":
    generate_weather()
