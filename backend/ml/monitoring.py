import os
import pandas as pd
from datetime import datetime

LOG_DIR = "ml/monitoring_logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "predictions.csv")


def log_prediction(input_data: dict, predictions: dict):
    """
    Logs each prediction request and response
    """

    record = {
        "timestamp": datetime.utcnow(),
        **input_data,
        **predictions
    }

    df = pd.DataFrame([record])

    if os.path.exists(LOG_FILE):
        df.to_csv(LOG_FILE, mode="a", header=False, index=False)
    else:
        df.to_csv(LOG_FILE, index=False)
