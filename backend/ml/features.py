import pandas as pd
import numpy as np

def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create ML-ready features from raw data.
    """

    features = df.copy()

    # Time-series inspired features
    features["recency"] = features["days_since_last_visit"]
    features["frequency"] = features["visits"]
    features["monetary"] = features["total_spend"]

    # Trend proxy (simple)
    features["engagement_score"] = (
        features["frequency"] /
        (features["recency"] + 1)
    )

    # Drop identifiers
    features = features.drop(columns=["customer_id"])

    return features
