import base64
from io import BytesIO

from fastapi import FastAPI
import matplotlib.pyplot as plt
import pandas as pd
from pydantic import BaseModel
import shap

from model_utils import load_model, predict


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
    GrAppv: float
    SBA_Appv: float

class PredictionOutput(BaseModel):
    category: str
    probability: float
    shap_plot: str

model= load_model()

@app.post("/predict")
def prediction_route(feature_input: FeaturesInput):
    # feats have here to be a pandas DataFrame
    # in order for the ColumnTransformer to properly work
    dump = feature_input.model_dump()
    del dump['ApprovalDoW']
    del dump['ApprovalMonth']
    del dump['CreateJob']
    inputs = pd.DataFrame(dump, index=[0])
    print("=====>", f"{inputs.shape = }")
    print("=====>", f"{inputs.columns = }")
    pred, prob, shap_values = predict(model, inputs)

    # Create the SHAP Waterfall plot
    shap.plots.waterfall(shap_values[0], show=False)
    buf = BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)
    base64_img = base64.b64encode(buf.read()).decode('utf-8')

    return PredictionOutput(category=pred, probability=prob, shap_plot=base64_img)
