import pandas as pd
import numpy as np

def load_data(n_customers: int = 1000) -> pd.DataFrame:
    """
    Generate synthetic customer transaction data.
    This simulates real business data for ML training.
    """

    np.random.seed(42)

    data = pd.DataFrame({
        "customer_id": range(n_customers),
        "visits": np.random.poisson(lam=5, size=n_customers),
        "avg_gap_days": np.random.uniform(1, 30, size=n_customers),
        "days_since_last_visit": np.random.uniform(1, 60, size=n_customers),
        "total_spend": np.random.uniform(50, 5000, size=n_customers),
    })

    # Regression target: days until next return
    data["days_until_return"] = (
        data["avg_gap_days"] +
        np.random.normal(0, 3, size=n_customers)
    ).clip(1)

    # Classification target: churn (1 = churned)
    data["churned"] = (data["days_since_last_visit"] > 30).astype(int)

    return data
