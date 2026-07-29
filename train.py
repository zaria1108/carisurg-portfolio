"""
Single entry point for training the pinned CariSurg triage model.

Usage:
    python scripts/train.py --config config.yaml

Reads every setting (data path, split, model choice, hyperparameters) from
config.yaml -- nothing about the pipeline is hardcoded here. This is the
file Martina Griffith's "new hire Monday morning" test is checking.
"""

import argparse
import json
import sys
from pathlib import Path

import joblib
from sklearn.model_selection import train_test_split

# Allow running this script directly from the scripts/ folder.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.data import load, clean
from src.features import build_xy, fit_transform_scaled
from src.model import build_model, train, evaluate
from src.utils import load_config, timer, per_prediction_ms


def main(config_path: str):
    config = load_config(config_path)

    # 1. Load + clean
    raw = load(config["data"]["raw_path"])
    df = clean(raw)
    print(f"Loaded and cleaned {df.shape[0]:,} rows, {df.shape[1]} columns.")

    # 2. Build features
    X, y = build_xy(df)
    print(f"Using {X.shape[1]} features to predict '{y.name}'.")

    # 3. Split (same seed as Week 6/7 for comparability)
    split_cfg = config["split"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=split_cfg["test_size"],
        stratify=y,
        random_state=split_cfg["random_state"],
    )
    print(f"Train: {X_train.shape[0]:,} rows | Test: {X_test.shape[0]:,} rows")

    # 4. Preprocess (scale only if the pinned model needs it)
    model_cfg = config["model"]
    if model_cfg.get("requires_scaling", False):
        X_train_final, X_test_final, imputer, scaler = fit_transform_scaled(X_train, X_test)
    else:
        X_train_final, X_test_final = X_train, X_test
        imputer, scaler = None, None

    # 5. Build + train, timed
    model = build_model(model_cfg["name"], model_cfg["params"])
    with timer() as train_timing:
        train(model, X_train_final, y_train)
    print(f"Trained '{model_cfg['name']}' in {train_timing['seconds']:.3f}s")

    # 6. Evaluate, timed
    with timer() as infer_timing:
        metrics = evaluate(model, X_test_final, y_test, esi1_label=config["data"]["esi1_label"])
    metrics["train_time_seconds"] = round(train_timing["seconds"], 3)
    metrics["inference_ms_per_patient"] = per_prediction_ms(infer_timing["seconds"], len(X_test_final))

    print("\n=== Evaluation ===")
    for k, v in metrics.items():
        print(f"  {k}: {v}")

    # 7. Persist model + metrics
    out_cfg = config["output"]
    Path(out_cfg["model_path"]).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"model": model, "imputer": imputer, "scaler": scaler}, out_cfg["model_path"])

    Path(out_cfg["metrics_path"]).parent.mkdir(parents=True, exist_ok=True)
    with open(out_cfg["metrics_path"], "w") as f:
        json.dump(metrics, f, indent=2)

    print(f"\nModel saved to {out_cfg['model_path']}")
    print(f"Metrics saved to {out_cfg['metrics_path']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train the pinned CariSurg triage model.")
    parser.add_argument("--config", default="config.yaml", help="Path to config.yaml")
    args = parser.parse_args()
    main(args.config)
