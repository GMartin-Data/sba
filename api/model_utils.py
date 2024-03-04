from typing import Tuple

import joblib
import pandas as pd


def load_model(path: str = "model.joblib"):
    model = joblib.load(path)
    return model

def predict(model, data: pd.DataFrame) -> Tuple[str, float]:
    verdict = ["Rejected", "Approved"]
    pred = model.predict(data)[0]
    prob = round(model.predict_proba(data)[0][pred] * 100, 2)
    return verdict[pred], prob
