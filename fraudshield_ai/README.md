# 🛡️ FraudShield AI

AI-powered financial fraud detection system built with Django + Machine Learning.

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run migrations
python manage.py migrate

# 3. Start server
python manage.py runserver
```

Then open http://127.0.0.1:8000

## 🔐 Auth Flow
1. Sign up at /accounts/signup/
2. Log in at /accounts/login/
3. **OTP is printed in the terminal** — enter it at /accounts/verify-otp/
4. You're in the dashboard!

## 📁 Structure
```
fraudguard_ai/        ← Django project settings
apps/
  accounts/           ← Auth, OTP
  dashboard/          ← Stats overview
  transactions/       ← ML fraud detection
  about/              ← Public pages
ml_models/
  fraud_model.pkl     ← Random Forest
  scaler.pkl          ← StandardScaler
  anomaly.pkl         ← Isolation Forest
templates/            ← All HTML templates
static/               ← CSS, JS
```

## 🤖 ML Models
- **Random Forest Classifier**: Primary fraud detection
- **Isolation Forest**: Anomaly detection layer
- **StandardScaler**: Feature normalization

OTP expires in 5 minutes. Re-login to get a new one.
