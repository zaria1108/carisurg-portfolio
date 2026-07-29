"""
Sanity-check tests for the CariSurg triage pipeline.

These two tests exist to make the pipeline break LOUDLY, not to prove the
code is perfect (Week 8 brief). Run with:

    pytest tests/ -v
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.data import clean, tiny_clean
from src.model import build_model, train


def test_clean_produces_valid_schema():
    """After cleaning, is the data the shape the model expects? Check the contract."""
    import pandas as pd
    import numpy as np

    # Minimal raw frame exercising the cleaning rules directly.
    raw = pd.DataFrame({
        "esi": [1, 2, 3, 4, 5, 99],          # 99 is an invalid label -> must be dropped
        "gender": ["Female", "Male", "Female", "Male", "Female", "Male"],
        "triage_vital_hr": [80, np.nan, 90, 75, 88, 95],  # one gap -> must be imputed
    })

    df = clean(raw)

    assert df["esi"].isin([1, 2, 3, 4, 5]).all()          # only valid labels survive
    assert df["triage_vital_hr"].isna().sum() == 0          # no gaps after imputation
    assert set(df["gender"].dropna().unique()) <= {0, 1}    # gender is encoded, not text


def test_smoke_train_predict():
    """Does the whole pipeline run on a tiny slice without crashing?
    Train on ~60 rows and predict -- this must always run in well under a second.
    """
    from sklearn.model_selection import train_test_split

    X, y = tiny_clean(60)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    model = build_model("random_forest", {"n_estimators": 20, "random_state": 42})
    train(model, X_train, y_train)
    preds = model.predict(X_test)

    assert len(preds) == len(y_test)  # ran end-to-end, correct output shape
