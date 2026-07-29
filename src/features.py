"""
Feature engineering for the CariSurg ED triage model.

Owns feature selection (which columns become model inputs) and any
encoding/scaling required before a model can be trained. Cleaning
(imputation, type coercion) happens upstream in data.py -- this module
assumes it receives already-clean data.
"""

import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

from src.data import VITALS, TARGET, LEAKAGE_COLS

# Columns intentionally excluded from every model, beyond leakage:
# demographics are excluded from model INPUTS to avoid encoding bias
# directly into triage recommendations (see Week 5 feasibility memo,
# "Demographic imbalance and potential bias"). They remain available
# in the cleaned DataFrame for fairness auditing, just not as features.
DEMOGRAPHIC_COLS = [
    "age", "gender", "ethnicity", "race", "lang", "religion",
    "maritalstatus", "employstatus", "insurance_status",
]
ADMIN_COLS = ["dep_name", "arrivalmode", "arrivalmonth", "arrivalday", "arrivalhour_bin"]


def select_features(df: pd.DataFrame) -> list[str]:
    """Return the list of column names used as model input.

    Excludes the target, leakage columns, demographics, and admin/logistics
    fields -- leaving vitals and chief-complaint (cc_*) flags only.
    """
    excluded = {TARGET, *LEAKAGE_COLS, *DEMOGRAPHIC_COLS, *ADMIN_COLS}
    return [c for c in df.columns if c not in excluded]


def build_xy(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """Split a cleaned DataFrame into (X, y) using the fixed feature set."""
    features = select_features(df)
    X = df[features]
    y = df[TARGET]
    return X, y


def make_preprocessor():
    """Return a fit-able (imputer, scaler) pair for scale-sensitive models.

    Tree-based models (decision tree, random forest) don't need scaling and
    can use X directly. Logistic regression and any distance-based model
    should run X through this preprocessor first.
    """
    imputer = SimpleImputer(strategy="median")
    scaler = StandardScaler()
    return imputer, scaler


def fit_transform_scaled(X_train: pd.DataFrame, X_test: pd.DataFrame):
    """Impute (median) then scale, fitting only on X_train.

    Returns (X_train_scaled, X_test_scaled, imputer, scaler) so the fitted
    objects can be persisted alongside the model for inference-time reuse.
    """
    imputer, scaler = make_preprocessor()
    X_train_imputed = imputer.fit_transform(X_train)
    X_test_imputed = imputer.transform(X_test)

    X_train_scaled = scaler.fit_transform(X_train_imputed)
    X_test_scaled = scaler.transform(X_test_imputed)

    return X_train_scaled, X_test_scaled, imputer, scaler
