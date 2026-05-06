#!/usr/bin/env python3
"""Train/eval multiclass severity model + SHAP + error export."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import shap
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.inspection import permutation_importance
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "analytics_stack" / "published" / "crossings_grain_demo.csv"
ART = ROOT / "modeling" / "artifacts"


def main() -> int:
    if not DATA.exists():
        print("Missing", DATA, file=sys.stderr)
        return 1
    ART.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(DATA)
    X = df[["State", "Year", "Warning_Device"]]
    y = df["Severity_Bucket"].astype(int)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.28, random_state=42, stratify=y
    )
    cat = ["State", "Warning_Device"]
    pre = ColumnTransformer(
        [("ohe", OneHotEncoder(handle_unknown="ignore"), cat)],
        remainder="passthrough",
    )
    models = {
        "baseline_most_frequent": DummyClassifier(strategy="most_frequent"),
        "baseline_stratified": DummyClassifier(strategy="stratified", random_state=42),
        "logreg_multinomial": LogisticRegression(max_iter=800),
        "random_forest": RandomForestClassifier(
            n_estimators=120, max_depth=12, random_state=42, class_weight="balanced"
        ),
    }
    metrics: dict = {}
    best_name = "random_forest"
    best_clf = None
    for name, est in models.items():
        pipe = Pipeline([("pre", pre), ("clf", est)])
        pipe.fit(X_train, y_train)
        pred = pipe.predict(X_test)
        metrics[name] = {
            "accuracy": float(accuracy_score(y_test, pred)),
            "macro_f1": float(f1_score(y_test, pred, average="macro")),
        }
        if name == best_name:
            best_clf = pipe
            y_pred = pred
    assert best_clf is not None
    (ART / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    labels = sorted(y.unique())
    cm = confusion_matrix(y_test, y_pred, labels=labels)
    fig, ax = plt.subplots(figsize=(5, 4))
    im = ax.imshow(cm, cmap="Blues")
    ax.set_xticks(range(len(labels)), labels=[str(x) for x in labels])
    ax.set_yticks(range(len(labels)), labels=[str(x) for x in labels])
    ax.set_xlabel("Predicted")
    ax.set_ylabel("True")
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, str(cm[i, j]), ha="center", va="center", color="black")
    fig.colorbar(im, ax=ax, fraction=0.046)
    fig.tight_layout()
    fig.savefig(ART / "confusion_matrix.png", dpi=120)
    plt.close()
    report = classification_report(y_test, y_pred, labels=labels, digits=3)
    (ART / "classification_report.txt").write_text(report, encoding="utf-8")
    err = X_test.copy()
    err["y_true"] = y_test.values
    err["y_pred"] = y_pred
    err = err[err["y_true"] != err["y_pred"]]
    err.head(200).to_csv(ART / "error_sample.csv", index=False)
    result = permutation_importance(
        best_clf, X_test, y_test, n_repeats=8, random_state=42, n_jobs=-1
    )
    (ART / "permutation_importance.json").write_text(
        json.dumps({"importances_mean": result.importances_mean.tolist()}, indent=2),
        encoding="utf-8",
    )
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.barh(range(len(result.importances_mean)), result.importances_mean)
    ax.set_yticks(range(len(result.importances_mean)))
    ax.set_yticklabels([f"f{i}" for i in range(len(result.importances_mean))])
    ax.set_xlabel("Mean acc drop")
    fig.tight_layout()
    fig.savefig(ART / "permutation_importance.png", dpi=120)
    plt.close()
    if os.environ.get("CI") != "1":
        try:
            forest: RandomForestClassifier = best_clf.named_steps["clf"]
            X_test_t = best_clf.named_steps["pre"].transform(X_test)
            explainer = shap.TreeExplainer(forest)
            sub = X_test_t[: min(500, X_test_t.shape[0])]
            sv = explainer.shap_values(sub, check_additivity=False)
            if isinstance(sv, list):
                sv_abs = np.mean([np.abs(s) for s in sv], axis=0)
                shap.summary_plot(
                    sv_abs,
                    sub,
                    plot_type="bar",
                    max_display=15,
                    show=False,
                )
            else:
                shap.summary_plot(
                    np.abs(sv),
                    sub,
                    plot_type="bar",
                    max_display=15,
                    show=False,
                )
            plt.tight_layout()
            plt.savefig(ART / "shap_summary.png", dpi=120, bbox_inches="tight")
            plt.close()
        except Exception as exc:
            print("SHAP skipped:", exc, file=sys.stderr)
    print("Wrote artifacts to", ART)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
