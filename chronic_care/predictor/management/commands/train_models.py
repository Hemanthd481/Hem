from django.core.management.base import BaseCommand
from pathlib import Path
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

from predictor.utils import REQUIRED_FEATURES, MODELS_DIR

DATASETS_DIR = Path(__file__).resolve().parents[3] / 'predictor' / 'datasets'


class Command(BaseCommand):
    help = 'Train RandomForest models for all supported diseases using datasets in predictor/datasets'

    def handle(self, *args, **options):
        MODELS_DIR.mkdir(parents=True, exist_ok=True)
        results = {}

        # Diabetes dataset
        try:
            df = pd.read_csv(DATASETS_DIR / 'diabetes.csv')
            X = df[REQUIRED_FEATURES['diabetes']]
            y = df['Outcome'] if 'Outcome' in df.columns else df['outcome']
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            model = RandomForestClassifier(n_estimators=200, random_state=42)
            model.fit(X_train, y_train)
            acc = accuracy_score(y_test, model.predict(X_test))
            joblib.dump(model, MODELS_DIR / 'diabetes_model.pkl')
            results['diabetes'] = acc
        except Exception as e:
            self.stderr.write(f"Diabetes training failed: {e}")

        # Heart disease dataset
        try:
            df = pd.read_csv(DATASETS_DIR / 'heart.csv')
            X = df[REQUIRED_FEATURES['heart']]
            y = df['target'] if 'target' in df.columns else df['Target']
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            model = RandomForestClassifier(n_estimators=200, random_state=42)
            model.fit(X_train, y_train)
            acc = accuracy_score(y_test, model.predict(X_test))
            joblib.dump(model, MODELS_DIR / 'heart_model.pkl')
            results['heart'] = acc
        except Exception as e:
            self.stderr.write(f"Heart training failed: {e}")

        # Kidney disease dataset (binary outcome column name 'class' -> 0/1 assumed)
        try:
            df = pd.read_csv(DATASETS_DIR / 'kidney.csv')
            X = df[REQUIRED_FEATURES['kidney']]
            y = df['class'] if 'class' in df.columns else df['target']
            if y.dtype == 'O':
                y = y.map({"ckd": 1, "notckd": 0, "ckd\t": 1}).fillna(0).astype(int)
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            model = RandomForestClassifier(n_estimators=200, random_state=42)
            model.fit(X_train, y_train)
            acc = accuracy_score(y_test, model.predict(X_test))
            joblib.dump(model, MODELS_DIR / 'kidney_model.pkl')
            results['kidney'] = acc
        except Exception as e:
            self.stderr.write(f"Kidney training failed: {e}")

        if results:
            self.stdout.write(self.style.SUCCESS(f"Training complete. Accuracies: {results}"))
        else:
            self.stderr.write("No models were trained. Check datasets.")