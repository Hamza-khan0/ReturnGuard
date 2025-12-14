from sklearn.metrics import (
    accuracy_score,
    f1_score,
    mean_squared_error
)
import numpy as np

def evaluate_classification(y_true, y_pred):
    return {
        "accuracy": accuracy_score(y_true, y_pred),
        "f1": f1_score(y_true, y_pred)
    }

def evaluate_regression(y_true, y_pred):
    return {
        "rmse": np.sqrt(mean_squared_error(y_true, y_pred))
    }
