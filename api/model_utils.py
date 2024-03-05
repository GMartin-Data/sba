from typing import Tuple

import joblib
import pandas as pd


def load_model_and_explainer(model_path: str = "model2.joblib", explainer_path: str = "explainer.joblib"):
    model = joblib.load(model_path)
    explainer = joblib.load(explainer_path)
    return model, explainer

def predict(model, explainer, data: pd.DataFrame) -> Tuple[str, float, 'shap_values']:
    verdict = ["Rejected", "Approved"]
    # Predicted Class
    pred = model.predict(data)[0]
    # Associated Probability
    prob = round(model.predict_proba(data)[0][pred] * 100, 2)
    # Generate SHAP values
    shap_values = explainer(data)

    return verdict[pred], prob, shap_values
