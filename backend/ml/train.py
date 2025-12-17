import os
import joblib

from ml.data_loader import load_data
from ml.features import build_features
from ml.schema import (
    FEATURE_COLUMNS,
    TARGET_REGRESSION,
    TARGET_CLASSIFICATION,
)

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score, f1_score, mean_squared_error
import numpy as np


def main():
    print("Loading World Bank data...")
    df = load_data()

    print("Building time-series features...")
    dataset = build_features(df, training=True)

    # -----------------------------
    # SPLIT FEATURES & TARGETS
    # -----------------------------
    X = dataset[FEATURE_COLUMNS]
    y_cls = dataset[TARGET_CLASSIFICATION]
    y_reg = dataset[TARGET_REGRESSION]

    # -----------------------------
    # TRAIN / TEST SPLIT
    # -----------------------------
    X_train, X_test, y_cls_train, y_cls_test = train_test_split(
        X, y_cls, test_size=0.2, random_state=42, shuffle=True
    )

    _, _, y_reg_train, y_reg_test = train_test_split(
        X, y_reg, test_size=0.2, random_state=42, shuffle=True
    )

    # -----------------------------
    # CLASSIFICATION MODEL
    # Economic Risk Prediction
    # -----------------------------
    print("Training classification model...")
    cls_model = LogisticRegression(max_iter=1000)
    cls_model.fit(X_train, y_cls_train)

    cls_preds = cls_model.predict(X_test)
    print(
        "Economic Risk Model:",
        {
            "accuracy": accuracy_score(y_cls_test, cls_preds),
            "f1": f1_score(y_cls_test, cls_preds),
        },
    )

    # -----------------------------
    # REGRESSION MODEL
    # GDP Growth Prediction
    # -----------------------------
    print("Training regression model...")
    reg_model = RandomForestRegressor(
        n_estimators=200,
        random_state=42
    )
    reg_model.fit(X_train, y_reg_train)

    reg_preds = reg_model.predict(X_test)
    print(
        "GDP Growth Model:",
        {
            "rmse": np.sqrt(mean_squared_error(y_reg_test, reg_preds))
        },
    )

    # -----------------------------
    # CLUSTERING
    # Economic Segments
    # -----------------------------
    print("Training clustering model...")
    kmeans = KMeans(n_clusters=3, n_init=10, random_state=42)
    clusters = kmeans.fit_predict(X)

    # -----------------------------
    # PCA
    # Visualization / Analysis
    # -----------------------------
    pca = PCA(n_components=2)
    pca_features = pca.fit_transform(X)

    # -----------------------------
    # SAVE MODELS
    # -----------------------------
    model_dir = "ml/models"
    os.makedirs(model_dir, exist_ok=True)

    joblib.dump(cls_model, f"{model_dir}/economic_risk_model.pkl")
    joblib.dump(reg_model, f"{model_dir}/gdp_growth_model.pkl")
    joblib.dump(kmeans, f"{model_dir}/cluster_model.pkl")
    joblib.dump(pca, f"{model_dir}/pca_model.pkl")

    print("\n=== TRAINING COMPLETE ===")
    print("Clusters:", set(clusters))
    print("PCA shape:", pca_features.shape)


if __name__ == "__main__":
    main()
