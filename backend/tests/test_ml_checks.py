import os
os.environ["DEEP_CHECKS_NO_DISPLAY"] = "1"

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression

from deepchecks.tabular import Dataset
from deepchecks.tabular.checks import TrainTestFeatureDrift, TrainTestPerformance


# ---------- Dummy Dataset ----------
X = pd.DataFrame({
    "visits": np.random.randint(1, 10, 100),
    "avg_gap_days": np.random.uniform(1, 15, 100),
    "days_since_last_visit": np.random.randint(1, 30, 100),
    "total_spend": np.random.uniform(50, 500, 100)
})

y = np.random.randint(0, 2, 100)

X_train = X.iloc[:80].reset_index(drop=True)
y_train = y[:80]

X_test = X.iloc[80:].reset_index(drop=True)
y_test = y[80:]

train_ds = Dataset(X_train, label=y_train)
test_ds = Dataset(X_test, label=y_test)


# ---------- Train lightweight CI model ----------
ci_model = LogisticRegression()
ci_model.fit(X_train, y_train)


# ---------- Tests ----------
def test_feature_drift():
    check = TrainTestFeatureDrift()
    result = check.run(train_ds, test_ds)
    assert result is not None


def test_model_performance():
    check = TrainTestPerformance()
    result = check.run(train_ds, test_ds, model=ci_model)
    assert result is not None
