"""
Data loading and cleaning for the CariSurg ED triage model.

This module owns exactly two responsibilities:
  1. load()  -- read the raw CSV into a DataFrame.
  2. clean() -- apply the cleaning rules established in Weeks 5-6
                (leakage-column removal, type coercion, imputation).

Nothing in this file should be specific to any one model; feature
engineering (encoding, feature selection) lives in features.py instead.
"""

from pathlib import Path
import pandas as pd
import numpy as np

# Columns known only AFTER triage -- excluded everywhere to prevent leakage
# (see Week 5 feasibility memo and Week 6 baseline report for rationale).
LEAKAGE_COLS = ["disposition", "previousdispo"]

# Vital-sign columns that must be numeric and complete before modelling.
VITALS = [
    "triage_vital_hr", "triage_vital_sbp", "triage_vital_dbp", "triage_vital_rr",
    "triage_vital_o2", "triage_vital_temp", "triage_glucose",
]

TARGET = "esi"


def load(path: str | Path) -> pd.DataFrame:
    """Read the raw triage extract from disk.

    Parameters
    ----------
    path : str or Path
        Location of the CSV export (e.g. yaleemmlc_admissionprediction_triage.csv).

    Returns
    -------
    pd.DataFrame
        Raw data, unmodified except for pandas' own type inference.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(
            f"Could not find {path}. Place the CSV beside this script, "
            f"or pass the correct path via config.yaml -> data.raw_path."
        )
    return pd.read_csv(path, index_col=0)


def clean(raw: pd.DataFrame) -> pd.DataFrame:
    """Apply the Week 5-6 cleaning rules to a raw DataFrame.

    Steps:
      - Drop rows with no target label (esi must be 1-5).
      - Coerce vital-sign columns to numeric, imputing missing values with
        the column median (documented, defensible default for a baseline).
      - Encode gender as a 0/1 column (Female=0, Male=1) for downstream
        schema consistency checks.

    Leakage columns are NOT dropped here -- that happens in features.py,
    so this function's output still contains every original column and
    can be reused for exploratory work that needs disposition, etc.
    """
    df = raw.copy()

    # 1. Target must be a valid ESI level
    df = df[df[TARGET].isin([1, 2, 3, 4, 5])].copy()

    # 2. Vitals: coerce to numeric, impute missing with median
    for col in VITALS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
            median = df[col].median()
            df[col] = df[col].fillna(median)

    # 3. Encode gender to 0/1 for schema consistency (Female=0, Male=1).
    # Note: checked via a trial map + isna, not dtype comparison, because
    # pandas 3.0 introduced a native "str" dtype distinct from "object" --
    # a dtype-equality check alone would silently miss modern string columns.
    if "gender" in df.columns:
        mapped = df["gender"].map({"Female": 0, "Male": 1, 0: 0, 1: 1})
        if mapped.notna().sum() > 0:
            df["gender"] = mapped.astype("Int64")

    return df


def tiny_clean(n_rows: int = 60) -> tuple[pd.DataFrame, pd.Series]:
    """Build a tiny synthetic dataset for fast smoke-testing.

    Used by tests/test_model_smoke.py so the test suite never depends on
    the full ~55k-row dataset being present on the test runner.
    """
    rng = np.random.default_rng(42)
    n = n_rows

    df = pd.DataFrame({
        "esi": rng.choice([1, 2, 3, 4, 5], size=n, p=[0.02, 0.3, 0.45, 0.18, 0.05]),
        "gender": rng.choice([0, 1], size=n),
        "triage_vital_hr": rng.normal(85, 15, size=n),
        "triage_vital_sbp": rng.normal(130, 20, size=n),
        "triage_vital_dbp": rng.normal(78, 12, size=n),
        "triage_vital_rr": rng.normal(18, 3, size=n),
        "triage_vital_o2": rng.normal(97, 2, size=n),
        "triage_vital_temp": rng.normal(98.2, 0.8, size=n),
        "triage_glucose": rng.normal(110, 30, size=n),
        "cc_abdominalpain": rng.choice([0, 1], size=n, p=[0.85, 0.15]),
        "cc_chestpain": rng.choice([0, 1], size=n, p=[0.9, 0.1]),
    })

    X = df.drop(columns=["esi"])
    y = df["esi"]
    return X, y
