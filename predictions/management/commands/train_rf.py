import json
from pathlib import Path
from typing import Optional

from django.core.management.base import BaseCommand, CommandParser
from joblib import dump
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


class Command(BaseCommand):
    help = 'Train a RandomForest classifier from a CSV (last column as target) and save to predictions/rf_model.joblib'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('--csv', required=True, help='Path to CSV file; header required')
        parser.add_argument('--target', default=None, help='Target column name (default: last column)')
        parser.add_argument('--n-estimators', type=int, default=200)
        parser.add_argument('--test-size', type=float, default=0.2)
        parser.add_argument('--random-state', type=int, default=42)

    def handle(self, *args, **options):
        csv_path = Path(options['csv'])
        target: Optional[str] = options['target']
        n_estimators: int = options['n_estimators']
        test_size: float = options['test_size']
        random_state: int = options['random_state']

        try:
            import csv
            with csv_path.open('r', newline='') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Failed to read CSV: {e}'))
            return

        if not rows:
            self.stderr.write(self.style.ERROR('CSV is empty'))
            return

        header = list(rows[0].keys())
        if target is None:
            target = header[-1]
        if target not in header:
            self.stderr.write(self.style.ERROR(f'Target {target} not found in header'))
            return

        feature_names = [h for h in header if h != target]
        X = np.array([[float(r[h]) for h in feature_names] for r in rows], dtype=float)
        y = np.array([int(float(r[target])) for r in rows])

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
        model = RandomForestClassifier(n_estimators=n_estimators, random_state=random_state)
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        acc = accuracy_score(y_test, preds)

        model_path = Path(__file__).resolve().parents[2] / 'rf_model.joblib'
        dump(model, model_path)
        meta_path = model_path.with_suffix('.json')
        meta = {'feature_names': feature_names, 'target': target, 'accuracy': float(acc)}
        meta_path.write_text(json.dumps(meta, indent=2))

        self.stdout.write(self.style.SUCCESS(f'Model saved to {model_path}'))
        self.stdout.write(self.style.SUCCESS(f'Meta saved to {meta_path}'))
        self.stdout.write(self.style.SUCCESS(f'Accuracy: {acc:.4f}'))