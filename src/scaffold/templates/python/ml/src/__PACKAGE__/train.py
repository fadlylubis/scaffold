"""Train a model and save it to models/. Swap load_data() for your dataset."""

import argparse
import logging
from pathlib import Path

import joblib
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

log = logging.getLogger(__name__)


def load_data():
    return load_iris(return_X_y=True)


def train(seed: int = 42) -> tuple[RandomForestClassifier, float]:
    X, y = load_data()
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=seed, stratify=y)
    model = RandomForestClassifier(random_state=seed).fit(X_tr, y_tr)
    return model, accuracy_score(y_te, model.predict(X_te))


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    p = argparse.ArgumentParser()
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--out", type=Path, default=Path("models/model.joblib"))
    args = p.parse_args()
    model, acc = train(args.seed)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, args.out)
    log.info("accuracy=%.3f saved=%s", acc, args.out)


if __name__ == "__main__":
    main()
