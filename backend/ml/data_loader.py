import requests
import pandas as pd

from ml.schema import (
    WORLD_BANK_INDICATORS,
    ENTITY_COLUMN,
    TIME_COLUMN
)

BASE_URL = "https://api.worldbank.org/v2/country"


def fetch_indicator(country: str, indicator_code: str, indicator_name: str) -> pd.DataFrame:
    """
    Fetch time-series data for a single World Bank indicator
    """
    url = f"{BASE_URL}/{country}/indicator/{indicator_code}"
    params = {
        "format": "json",
        "per_page": 1000
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    if not data or len(data) < 2:
        return pd.DataFrame()

    records = data[1]

    rows = []
    for r in records:
        if r["value"] is not None:
            rows.append({
                ENTITY_COLUMN: country,
                TIME_COLUMN: int(r["date"]),
                indicator_name: float(r["value"])
            })

    return pd.DataFrame(rows)


def load_data(countries=None) -> pd.DataFrame:
    """
    Load and merge World Bank indicators into a single DataFrame
    """
    if countries is None:
        countries = ["USA", "PAK", "IND", "GBR", "CHN"]

    all_data = []

    for country in countries:
        country_df = None

        for feature_name, indicator_code in WORLD_BANK_INDICATORS.items():
            df = fetch_indicator(
                country=country,
                indicator_code=indicator_code,
                indicator_name=feature_name
            )

            if df.empty:
                continue

            if country_df is None:
                country_df = df
            else:
                country_df = country_df.merge(
                    df,
                    on=[ENTITY_COLUMN, TIME_COLUMN],
                    how="inner"
                )

        if country_df is not None:
            all_data.append(country_df)

    final_df = pd.concat(all_data, ignore_index=True)

    # Sort for time-series feature engineering
    final_df = final_df.sort_values(
        by=[ENTITY_COLUMN, TIME_COLUMN]
    ).reset_index(drop=True)

    return final_df
