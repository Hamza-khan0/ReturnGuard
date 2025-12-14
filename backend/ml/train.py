import joblib
import os

from data_loader import load_data
from features import build_features
from evaluate import evaluate_classification, evaluate_regression

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

def main():
    # Load and prepare data
    df = load_data()
    features = build_features(df)

    # -------- CLASSIFICATION (Churn) --------
    X_cls = features.drop(columns=["churned", "days_until_return"])
    y_cls = features["churned"]

    Xc_train, Xc_test, yc_train, yc_test = train_test_split(
        X_cls, y_cls, test_size=0.2, random_state=42
    )

    churn_model = LogisticRegression(max_iter=1000)
    churn_model.fit(Xc_train, yc_train)

    churn_preds = churn_model.predict(Xc_test)
    cls_metrics = evaluate_classification(yc_test, churn_preds)

    # -------- REGRESSION (Return Time) --------
    X_reg = features.drop(columns=["churned", "days_until_return"])
    y_reg = features["days_until_return"]

    Xr_train, Xr_test, yr_train, yr_test = train_test_split(
        X_reg, y_reg, test_size=0.2, random_state=42
    )

    return_model = RandomForestRegressor(random_state=42)
    return_model.fit(Xr_train, yr_train)

    return_preds = return_model.predict(Xr_test)
    reg_metrics = evaluate_regression(yr_test, return_preds)

    # -------- CLUSTERING --------
    kmeans = KMeans(n_clusters=3, random_state=42)
    clusters = kmeans.fit_predict(X_reg)

    # -------- PCA --------
    pca = PCA(n_components=2)
    pca_features = pca.fit_transform(X_reg)

        # -------- SAVE MODELS --------
    os.makedirs("models", exist_ok=True)

    joblib.dump(churn_model, "models/churn_model.pkl")
    joblib.dump(return_model, "models/return_time_model.pkl")
    joblib.dump(kmeans, "models/cluster_model.pkl")
    joblib.dump(pca, "models/pca_model.pkl")

    print("\n=== TRAINING RESULTS ===")
    print("Churn Model:", cls_metrics)
    print("Return Time Model:", reg_metrics)
    print("Clusters created:", set(clusters))
    print("PCA shape:", pca_features.shape)

if __name__ == "__main__":
    main()
