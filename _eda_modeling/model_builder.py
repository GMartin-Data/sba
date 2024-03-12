"""
Script to build best model.
"""

from category_encoders import TargetEncoder
import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler
import xgboost as xgb


# LOAD DATAFRAME
df_short = pd.read_csv("data/cleaned_df_short.csv", index_col=0)

# BUILD MODEL
COLS_TO_DROP = ['City', 'CreateJob', 'LowDoc'] 

X = df_short.copy().drop(columns=COLS_TO_DROP)
y = X.pop("MIS_Status")

# Default stratify by y
X_train, X_test, y_train, y_test = \
train_test_split(X, y, test_size=0.05, stratify=y, random_state=42)

# Encode target
lab_enc = LabelEncoder()
y_train = lab_enc.fit_transform(y_train)
y_test = lab_enc.transform(y_test)

# Split kept columns
kept_set = set(X_train.columns)
num_cols = list({"Term", "NoEmp", "CreateJob", "RetainedJob", "GrAppv", "SBA_Appv"} & kept_set)
bin_cols = list({"SameState", "Recession", "NewExist", "Franchise",
                 "LowDoc", "UrbanRural", "RevLineCr"} & kept_set)
nom_cols = list({"Region", "NAICS"} & kept_set)
tgt_cols = list({"City", "Bank", "State", "BankState"} & kept_set)

# Instanciate transformers
std_scl = StandardScaler()
ohe_bin = OneHotEncoder(drop="if_binary", handle_unknown="ignore",
                        sparse_output=False)
ohe_nom = OneHotEncoder(handle_unknown="ignore",
                        sparse_output=False)
tgt_enc = TargetEncoder(smoothing=1.0)

# Pipeline
## Preprocessing
preproc = ColumnTransformer(
transformers = [
    ("num", std_scl, num_cols),
    ("bin", ohe_bin, bin_cols),
    ("nom", ohe_nom, nom_cols),
    ("tgt", tgt_enc, tgt_cols)
],
verbose_feature_names_out = False
)
preproc.set_output(transform="pandas")
## Append estimator
xgbc = xgb.XGBClassifier(random_state=42)
model = make_pipeline(preproc, xgbc)

# SET BEST HYPERPARAMETERS
best_params = {
    'xgbclassifier__colsample_bylevel': 0.5042897472548691, 
    'xgbclassifier__colsample_bytree': 0.6309376784120938,
    'xgbclassifier__eval_metric': 'logloss',
    'xgbclassifier__gamma': 0.00015032547632461585,
    'xgbclassifier__learning_rate': 0.01046761262328419,
    'xgbclassifier__max_delta_step': 10,
    'xgbclassifier__max_depth': 25,
    'xgbclassifier__n_estimators': 800,
    'xgbclassifier__objective': 'binary:logistic',
    'xgbclassifier__reg_alpha': 2.872268280704231e-09,
    'xgbclassifier__reg_lambda': 2.366591909619298e-05,
    'xgbclassifier__scale_pos_weight': 0.8283817065736674,
    'xgbclassifier__subsample': 0.554918889507587,
    'xgbclassifier__verbosity': 0
}

model.set_params(**best_params)

# TRAIN AND SCORE
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
raw_f1_macro = f1_score(y_test, y_pred, average="macro")
print(f"{raw_f1_macro = :.4f}")

# EXPORT MODEL
joblib.dump(model, "best_model.joblib")
