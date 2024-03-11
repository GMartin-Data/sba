from typing import Tuple

import joblib
import pandas as pd
import shap


def load_model(model_path: str = "short.joblib"):
    model = joblib.load(model_path)
    return model


def predict(model, data: pd.DataFrame) -> Tuple[str, float, 'shap_values']:
    """
    Output details about the prediction as a tuple, including:
    - The prediction as a string: "Rejected" or "Approved"
    - The corresponding probability.
    - The Shapley values, allowing to interpret the prediction,
    as the endpoint will use them to generate an encoded graph.
    """
    verdict = ["Rejected", "Approved"]
    # Predicted Class
    y_pred = model.predict(data)
    pred = y_pred[0]
    # Associated Probability
    prob = round(model.predict_proba(data)[0][pred] * 100, 2)
    # Generate SHAP values
    data_tr = model[:-1].transform(data)
    shap_explainer = shap.TreeExplainer(model[-1])
    shap_ = shap_explainer(data_tr)

    return verdict[pred], prob, shap_
