import base64
from io import BytesIO

from fastapi import FastAPI
import pandas as pd
from pydantic import BaseModel
import shap

from model_utils import load_model_and_explainer, predict


app = FastAPI()

class FeaturesInput(BaseModel):
    State: str
    Region: str
    Bank: str
    BankState: str
    SameState: bool
    NAICS: str
    ApprovalMonth: int
    ApprovalDoW: int
    Recession: bool
    Term: int
    NewExist: str
    NoEmp: int
    CreateJob: int
    RetainedJob: int
    Franchise: str
    UrbanRural: str
    RevLineCr: str
    LowDoc: str
    GrAppv: float
    SBA_Appv: float

class PredictionOutput(BaseModel):
    category: str
    probability: float
    shap_plot: str

model = load_model_and_explainer()

@app.post("/predict")
def prediction_route(feature_input: FeaturesInput):
    # feats have here to be a pandas DataFrame
    # in order for the ColumnTransformer to properly work
    inputs = pd.DataFrame(feature_input.model_dump(), index=[0])
    pred, prob, shap_values = predict(model, inputs)

    # Create the SHAP Waterfall plot
    shap.plots.waterfall(shap_values[0], show=False)

    return PredictionOutput(category=pred, probability=prob)
