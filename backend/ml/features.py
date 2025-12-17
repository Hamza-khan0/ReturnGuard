import pandas as pd
from ml.schema import FEATURE_COLUMNS, ENTITY_COLUMN, TIME_COLUMN


def build_features(df: pd.DataFrame, training: bool = False) -> pd.DataFrame:
    """
    Build ML-ready time-series features from World Bank data.
    """

    df = df.copy()

    # -----------------------------
    # Sort for time-series ops
    # -----------------------------
    df = df.sort_values([ENTITY_COLUMN, TIME_COLUMN])

    # -----------------------------
    # Ensure numeric types
    # -----------------------------
    for col in ["gdp", "inflation", "unemployment"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # -----------------------------
    # Lag features (1 year)
    # -----------------------------
    df["gdp_lag_1"] = df.groupby(ENTITY_COLUMN)["gdp"].shift(1)
    df["inflation_lag_1"] = df.groupby(ENTITY_COLUMN)["inflation"].shift(1)
    df["unemployment_lag_1"] = df.groupby(ENTITY_COLUMN)["unemployment"].shift(1)

    # -----------------------------
    # Rolling mean features (3 years)
    # NAMES MATCH schema.py EXACTLY
    # -----------------------------
    df["gdp_rolling_mean_3"] = (
        df.groupby(ENTITY_COLUMN)["gdp"]
        .rolling(window=3)
        .mean()
        .reset_index(level=0, drop=True)
    )

    df["inflation_rolling_mean_3"] = (
        df.groupby(ENTITY_COLUMN)["inflation"]
        .rolling(window=3)
        .mean()
        .reset_index(level=0, drop=True)
    )

    # Optional but safe (even if schema ignores it)
    df["unemployment_rolling_mean_3"] = (
        df.groupby(ENTITY_COLUMN)["unemployment"]
        .rolling(window=3)
        .mean()
        .reset_index(level=0, drop=True)
    )

    # -----------------------------
    # GDP growth (%)
    # -----------------------------
    df["gdp_growth"] = (
        df.groupby(ENTITY_COLUMN)["gdp"]
        .pct_change() * 100
    )

    # -----------------------------
    # TRAINING TARGETS ONLY
    # -----------------------------
    if training:
        df["gdp_growth_next_year"] = (
            df.groupby(ENTITY_COLUMN)["gdp_growth"].shift(-1)
        )

        df["economic_risk"] = (
            (df["inflation"] > 10) |
            (df["unemployment"] > 8)
        ).astype(int)

    # -----------------------------
    # Final dataset (schema-driven)
    # -----------------------------
    final_cols = FEATURE_COLUMNS.copy()

    if training:
        final_cols += ["gdp_growth_next_year", "economic_risk"]

    return df[final_cols].dropna()
