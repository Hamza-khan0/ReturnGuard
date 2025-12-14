from prefect import flow, task
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


@task(retries=2, retry_delay_seconds=5)
def ingest_data():
    return load_data()


@task
def feature_engineering(df):
    return build_features(df)


@task
def train_churn_model(X, y):
    model = LogisticRegression(max_iter=1000)
    model.fit(X, y)
    return model


@task
def train_return_model(X, y):
    model = RandomForestRegressor(random_state=42)
    model.fit(X, y)
    return model


@task
def evaluate_models(churn_model, return_model, X_test, y_cls_test, y_reg_test):
    churn_preds = churn_model.predict(X_test)
    return_preds = return_model.predict(X_test)

    cls_metrics = evaluate_classification(y_cls_test, churn_preds)
    reg_metrics = evaluate_regression(y_reg_test, return_preds)

    return cls_metrics, reg_metrics


@task
def save_models(churn_model, return_model, cluster_model, pca_model):
    os.makedirs("models", exist_ok=True)

    joblib.dump(churn_model, "models/churn_model.pkl")
    joblib.dump(return_model, "models/return_time_model.pkl")
    joblib.dump(cluster_model, "models/cluster_model.pkl")
    joblib.dump(pca_model, "models/pca_model.pkl")


@flow(name="ReturnGuard Training Pipeline")
def training_pipeline():
    # Ingest
    df = ingest_data()

    # Feature engineering
    features = feature_engineering(df)

    X = features.drop(columns=["churned", "days_until_return"])
    y_cls = features["churned"]
    y_reg = features["days_until_return"]

    X_train, X_test, y_cls_train, y_cls_test = train_test_split(
        X, y_cls, test_size=0.2, random_state=42
    )
    _, _, y_reg_train, y_reg_test = train_test_split(
        X, y_reg, test_size=0.2, random_state=42
    )

    # Train models
    churn_model = train_churn_model(X_train, y_cls_train)
    return_model = train_return_model(X_train, y_reg_train)

    # Clustering + PCA
    cluster_model = KMeans(n_clusters=3, random_state=42).fit(X)
    pca_model = PCA(n_components=2).fit(X)

    # Evaluation
    cls_metrics, reg_metrics = evaluate_models(
        churn_model, return_model, X_test, y_cls_test, y_reg_test
    )

    print("Classification metrics:", cls_metrics)
    print("Regression metrics:", reg_metrics)

    # Save models
    save_models(churn_model, return_model, cluster_model, pca_model)


if __name__ == "__main__":
    training_pipeline()
