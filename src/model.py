"""
Model building, training, and evaluation for the CariSurg ED triage model.

The Week 7 decision journal (docs/decisions/2026-week-7-model-choice.md)
pinned Logistic Regression as the Phase 3 model: it beat a Random Forest
on every accuracy metric, was the only model to achieve non-zero recall
on ESI Level 1, was ~29x faster at inference, and is explainable to a
clinician in one sentence. This module builds that model -- and, for the
audit trail, the other models benchmarked in Weeks 6-7 -- from a single
config so the choice is reproducible, not just described.
"""

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.dummy import DummyClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report,
)

# Registry of every model type benchmarked across Weeks 6-7.
# "logistic_regression" is the PINNED model per the Week 7 decision journal.
MODEL_REGISTRY = {
    "dummy": lambda params: DummyClassifier(**params),
    "logistic_regression": lambda params: LogisticRegression(**params),
    "decision_tree": lambda params: DecisionTreeClassifier(**params),
    "random_forest": lambda params: RandomForestClassifier(**params),
}


def build_model(model_name: str, params: dict):
    """Instantiate a model from the registry by name and hyperparameter dict.

    Parameters
    ----------
    model_name : str
        One of the keys in MODEL_REGISTRY (see config.yaml for the pinned choice).
    params : dict
        Hyperparameters passed straight to the sklearn constructor.
    """
    if model_name not in MODEL_REGISTRY:
        raise ValueError(
            f"Unknown model '{model_name}'. Valid options: {list(MODEL_REGISTRY)}"
        )
    return MODEL_REGISTRY[model_name](params)


def train(model, X_train, y_train):
    """Fit a model in place and return it (for chaining)."""
    model.fit(X_train, y_train)
    return model


def evaluate(model, X_test, y_test, esi1_label: int = 1) -> dict:
    """Compute the standard metric set used throughout Weeks 6-7.

    Returns a flat dict so results can be appended directly as a row in
    the model-selection results table (docs/model-selection.csv).
    """
    preds = model.predict(X_test)

    return {
        "accuracy": round(accuracy_score(y_test, preds), 3),
        "precision_macro": round(precision_score(y_test, preds, average="macro", zero_division=0), 3),
        "recall_macro": round(recall_score(y_test, preds, average="macro", zero_division=0), 3),
        "f1_macro": round(f1_score(y_test, preds, average="macro"), 3),
        "recall_esi1": round(
            recall_score(y_test, preds, labels=[esi1_label], average=None, zero_division=0)[0], 3
        ),
    }


def classification_report_text(model, X_test, y_test) -> str:
    """Full per-class report, for logging / handover appendix."""
    preds = model.predict(X_test)
    return classification_report(y_test, preds, digits=3, zero_division=0)
