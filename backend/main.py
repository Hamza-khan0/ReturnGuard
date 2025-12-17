import os
import joblib
import pandas as pd

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from ml.data_loader import load_data
from ml.features import build_features
from ml.schema import FEATURE_COLUMNS, ENTITY_COLUMN, TIME_COLUMN
from ml.monitoring import log_prediction   # ✅ ADDED

# ---------------- APP ----------------
app = FastAPI(title="Economic Forecast API")

# ---------------- MODEL PATHS ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "ml", "models")

# ---------------- LOAD MODELS ----------------
try:
    risk_model = joblib.load(os.path.join(MODEL_DIR, "economic_risk_model.pkl"))
    gdp_model = joblib.load(os.path.join(MODEL_DIR, "gdp_growth_model.pkl"))
    cluster_model = joblib.load(os.path.join(MODEL_DIR, "cluster_model.pkl"))
except FileNotFoundError as e:
    raise RuntimeError(
        f"Model file missing. Did you run `python -m ml.train`? → {e}"
    )

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- INPUT SCHEMA ----------------
class EconomyInput(BaseModel):
    country: str
    year: int
    gdp: float
    inflation: float
    unemployment: float

# ---------------- ROUTES ----------------
@app.get("/")
def health():
    return {"status": "API running"}

@app.post("/predict/economy")
def predict_economy(data: EconomyInput):

    # 1️⃣ Load historical World Bank data
    hist_df = load_data(countries=[data.country])

    if hist_df.empty:
        raise HTTPException(
            status_code=400,
            detail=f"No historical data found for country={data.country}"
        )

    # 2️⃣ Append latest year
    new_row = {
        ENTITY_COLUMN: data.country,
        TIME_COLUMN: data.year,
        "gdp": data.gdp,
        "inflation": data.inflation,
        "unemployment": data.unemployment,
    }

    df = pd.concat([hist_df, pd.DataFrame([new_row])], ignore_index=True)

    # 3️⃣ Build features
    features_df = build_features(df, training=False)

    if features_df.empty:
        raise HTTPException(
            status_code=400,
            detail="Not enough historical data to compute lag/rolling features"
        )

    # 4️⃣ Latest valid row
    X = features_df.tail(1)[FEATURE_COLUMNS]

    # 5️⃣ Feature sanity check
    if list(X.columns) != FEATURE_COLUMNS:
        raise HTTPException(
            status_code=500,
            detail=f"Feature mismatch. Expected {FEATURE_COLUMNS}, got {list(X.columns)}"
        )

    # 6️⃣ Predictions
    economic_risk = int(risk_model.predict(X)[0])
    gdp_next_year = float(gdp_model.predict(X)[0])
    cluster = int(cluster_model.predict(X)[0])

    response = {
        "economic_risk": economic_risk,
        "predicted_gdp_growth_next_year": round(gdp_next_year, 2),
        "economic_cluster": cluster,
    }

    # ✅ MONITORING (FAIL-SAFE)
    try:
        log_prediction(
            input_data=data.dict(),
            predictions=response
        )
    except Exception as e:
        print(f"[MONITORING WARNING] Logging failed: {e}")

    return response
