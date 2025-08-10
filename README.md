# Chronic Disease Predictor Platform

A ready-to-use Django web app for chronic disease prediction (multiple diseases) with Random Forest models, doctor (admin) and patient roles, announcements, chat, patient room allotment, and analytics using Chart.js.

## Features
- Doctor (admin):
  - Create patient profiles and manage patient list
  - View and reply to messages from patients
  - Post announcements to all patients
  - View disease prediction analytics (Chart.js)
  - Allot rooms to patients
- Patient:
  - View announcements on home page
  - 1:1 chat with doctor
  - View room allotment
  - Predict diseases and see results
- Prediction:
  - Random Forest models for multiple diseases (diabetes, heart disease, kidney disease)
  - Training script included; ships with small sample datasets

## Tech Stack
- Backend: Django, Python
- Frontend: HTML, CSS, JS, Bootstrap, Chart.js (CDN)
- ML: numpy, pandas, scikit-learn, joblib

## Quick Start

1. Install dependencies

```bash
python -m pip install --user -r requirements.txt
```

2. Create the project database and migrate

```bash
python /workspace/chronic_care/manage.py migrate
```

3. Create a superuser (doctor)

```bash
python /workspace/chronic_care/manage.py createsuperuser
```

4. Train ML models (Random Forest) using provided datasets

```bash
python /workspace/chronic_care/manage.py train_models
```

5. Run the server

```bash
python /workspace/chronic_care/manage.py runserver 0.0.0.0:8000
```

6. Log in
- Doctor: use the superuser credentials you created
- Patients: create from Doctor dashboard (Patients -> Create)

## Default URLs
- `/` — Role-aware home (redirects to doctor or patient dashboard)
- `/admin/` — Django admin
- `/accounts/` — Auth and role redirects
- `/patients/` — Patient management (doctor)
- `/announcements/` — Announcements
- `/chat/` — Messaging
- `/predict/` — Disease prediction
- `/dashboard/analytics/` — Chart.js analytics (doctor)

## Environment
- Uses SQLite by default (no setup needed). For Postgres/MySQL, install the appropriate driver (already in requirements) and edit `chronic_care/settings.py`.

## Notes
- Sample datasets are in `predictor/datasets`. Feel free to replace with your own datasets (matching column names) and re-run training.
- Models are saved under `predictor/disease_models`.
