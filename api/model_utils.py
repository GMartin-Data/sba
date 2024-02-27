import joblib
import pandas as pd


def load_model(path: str = "model.joblib"):
    model = joblib.load(path)
    return model

def predict(model, data: pd.DataFrame) -> str:
    predictions = model.predict(data)
    return "Approved" if predictions[0] else "Rejected"
