"""
Single source of truth for ML features and targets.
Used by:
- data_loader.py
- features.py
- train.py
- FastAPI inference
"""

# --------------------------------
# WORLD BANK INDICATORS (RAW)
# --------------------------------

WORLD_BANK_INDICATORS = {
    "gdp": "NY.GDP.MKTP.CD",          # GDP (current US$)
    "inflation": "FP.CPI.TOTL.ZG",    # Inflation (%)
    "unemployment": "SL.UEM.TOTL.ZS", # Unemployment (%)
}

# --------------------------------
# METADATA
# --------------------------------

TIME_COLUMN = "year"
ENTITY_COLUMN = "country"

# --------------------------------
# FEATURE COLUMNS (MODEL INPUT)
# MUST MATCH features.py EXACTLY
# --------------------------------

FEATURE_COLUMNS = [
    # Raw indicators
    "gdp",
    "inflation",
    "unemployment",

    # Lag features
    "gdp_lag_1",
    "inflation_lag_1",
    "unemployment_lag_1",

    # Rolling means (3-year window)
    "gdp_rolling_mean_3",
    "inflation_rolling_mean_3",
    "unemployment_rolling_mean_3",
]

# --------------------------------
# TARGETS
# --------------------------------

# Regression target
TARGET_REGRESSION = "gdp_growth_next_year"

# Classification target
TARGET_CLASSIFICATION = "economic_risk"
