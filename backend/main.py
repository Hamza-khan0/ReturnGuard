import os
import joblib
import numpy as np

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# ------------------ APP ------------------
app = FastAPI(title="ReturnGuard API")

# ------------------ LOAD ML MODELS AT STARTUP ------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "ml", "models")

churn_model = joblib.load(os.path.join(MODEL_DIR, "churn_model.pkl"))
return_model = joblib.load(os.path.join(MODEL_DIR, "return_time_model.pkl"))
cluster_model = joblib.load(os.path.join(MODEL_DIR, "cluster_model.pkl"))
pca_model = joblib.load(os.path.join(MODEL_DIR, "pca_model.pkl"))

# ------------------ CORS ------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------ INPUT SCHEMA ------------------
class CustomerInput(BaseModel):
    visits: int
    avg_gap_days: float
    days_since_last_visit: float
    total_spend: float

# ------------------ ROUTES ------------------
@app.get("/")
def health_check():
    return {"status": "ReturnGuard backend running"}

@app.post("/predict/customer")
def predict_customer(customer: CustomerInput):
    """
    Real ML inference endpoint
    """

    # Feature order MUST match training
    features = np.array([[
        customer.visits,
        customer.avg_gap_days,
        customer.days_since_last_visit,
        customer.total_spend
    ]])

    churn_pred = churn_model.predict(features)[0]
    return_time_pred = return_model.predict(features)[0]
    cluster_pred = cluster_model.predict(features)[0]

    return {
        "churn_prediction": int(churn_pred),
        "predicted_return_days": round(float(return_time_pred), 2),
        "customer_segment": int(cluster_pred)
    }
