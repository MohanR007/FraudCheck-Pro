# FraudCheck Pro – Unified Transaction Fraud Detection Platform

Modern, single-path Flask + vanilla JS web application for real‑time transaction fraud detection with enriched feature engineering, expanded risk vocabularies, and explainable outputs.

**Live Demo (Frontend Only):** https://fraudcheck-pro.netlify.app  
**Full Application (Backend + API on Render):** https://fraudcheck-pro.onrender.com  
> Netlify = static UI (expects local API unless configured).  
> Render = full stack (Flask backend + UI) - cold starts may add a short initial delay.

---
## ✨ Key Features
- 🧠 13-feature enhanced fraud scoring (amount, time, payment, geography, device, behavior, merchant, deviation)
- 🗺️ Country & region risk mapping (expanded high/medium tiers)
- 💳 Extended payment method taxonomy (cards, wallets, crypto, transfers)
- 🏪 Rich merchant category coverage with adaptive risk weighting
- 📊 Real-time dashboard & statistics (fraud rate, blocked amount, daily trend)
- 🕒 Time & frequency heuristics (unusual hours, velocity flags)
- 🔍 Explainable results: risk level + contributing reasons
- 🛡️ Heuristic fallback engine if ML model/scaler mismatch occurs
- 🧹 Clean, minimal codebase (legacy variants removed)
- 🧪 Scenario test matrix (`testcases.md` + API test script)

---
## 🗂 Project Structure (Unified)
```
fraudcheck-web/
├── backend/
│   ├── app.py                        # Flask application (single entrypoint)
│   └── requirements.txt              # Python dependencies
├── frontend/
│   └── index.html                    # Unified UI (dashboard + detector + history + analytics)
├── models/
│   ├── create_simple_working_model.py# Deterministic synthetic model trainer
│   ├── fraud_detection_model.pkl     # Saved RandomForest model
│   ├── scaler.pkl                    # Feature scaler
│   └── model_metadata.txt            # Basic model metadata
├── test_enhanced_api.py              # API smoke / scenario test script
├── testcases.md                      # Manual + structured test scenarios
├── setup.bat                         # Environment & model setup
├── run.bat                           # Launch script (runs app.py)
└── README.md
```
> Removed: legacy basic/enhanced splits, extra model scripts, unused HTML variants, redundant batch files.

---
## ⚡ Quick Start
### 1. Create & Activate Virtual Environment (Recommended)
```cmd
python -m venv venv
venv\Scripts\activate
```
### 2. Install Dependencies
```cmd
pip install --only-binary=all -r backend\requirements.txt
```
### 3. (Optional) Recreate Model
```cmd
cd models
python create_simple_working_model.py
cd ..
```
### 4. Run Application (Backend API)
```cmd
run.bat
```
Open: http://localhost:5000 (the UI is served + API endpoints).

---
## 🛰 API Example
```javascript
const res = await fetch('/api/predict', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    amount: 8500,
    payment_method: 'cryptocurrency',
    country: 'NG',
    device_info: 'mobile',
    ip_risk: 9,
    customer_age: 19,
    account_age: 5,
    daily_transactions: 14,
    avg_transaction: 120,
    merchant_category: 'gambling',
    transaction_time: '02:45'
  })
});
const data = await res.json();
```
Sample response:
```json
{
  "is_fraud": true,
  "fraud_probability": 0.92,
  "risk_level": "Very High",
  "fraud_reasons": [
    "High transaction amount",
    "High-risk country",
    "High-risk payment method",
    "High transaction frequency",
    "High-risk merchant category"
  ],
  "fallback_used": false
}
```

---
## 🧬 Feature Schema (13 Inputs → Engineered Vector)
Index | Description | Source Field(s)
------|-------------|----------------
0 | Normalized amount (capped) | amount
1 | High amount flag (>5000) | amount
2 | Hour of day | transaction_time
3 | Unusual hour flag (<6 or >22) | transaction_time
4 | Payment method risk score | payment_method
5 | Country/location risk | country
6 | Device risk score | device_info
7 | IP risk (scaled /10) | ip_risk
8 | Age risk flag (<21 or >65) | customer_age
9 | New account flag (<30 days) | account_age
10 | High frequency flag (>10/day) | daily_transactions
11 | Relative amount deviation | amount vs avg_transaction
12 | Merchant category risk | merchant_category

If the ML pipeline fails (dimension mismatch, scaler error), a rule-based heuristic assigns probability and sets `fallback_used: true`.

---
## 🔧 Runtime Endpoints
Endpoint | Method | Purpose
---------|--------|--------
`/` | GET | Unified web interface
`/api/predict` | POST | Fraud inference
`/api/health` | GET | Status & model load check
`/api/statistics` | GET | Aggregated metrics (fraud rate, totals)
`/api/reset-stats` | POST | Reset counters (testing)

---
## 🧪 Testing
Automated smoke / scenario test:
```cmd
python test_enhanced_api.py
```
Manual matrix: see `testcases.md` (low / medium / high risk + edge cases).

---
## 🔐 Security Notes (Development Mode)
- Dev Flask server only (add WSGI server + hardening for prod)
- CORS currently broad
- No auth (add API key / JWT before public exposure)
- Validate & sanitize upstream when integrating with real payment flows

---
## 🚢 Deployment Tips
- Use gunicorn/uvicorn behind Nginx or similar
- Disable `debug=True`
- Preload model on startup
- Add structured logging + request correlation IDs
- Consider model versioning & performance metrics export

### 🌐 Netlify Frontend Integration
The hosted frontend assumes same-origin API calls. To use remote APIs:
1. Expose your backend publicly (e.g., via a tunnel or deployment).
2. Replace fetch base paths in `index.html` with your API root (future enhancement: config variable).
3. Ensure CORS allows the Netlify origin.

---
## 🛠 Future Enhancements
- Threshold calibration (Platt / isotonic)
- Persistent stats store (SQLite/Postgres)
- Streaming ingestion adapter (Kafka / Kinesis)
- Case management & audit trail
- Adaptive / online model retraining hooks

---
## 📄 License
MIT – use freely with attribution.

FraudCheck Pro – streamlined, explainable, and extensible. 🛡️

---
## Tech Stack
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Backend**: Python Flask
- **ML Model**: scikit-learn Random Forest
- **Data Processing**: pandas, numpy
- **Persistence**: joblib artifacts (model + scaler)

---
## Contributing
1. Fork the repository
2. Create a feature branch
3. Make changes with clear commits
4. Add/Update tests where relevant
5. Open a Pull Request

---
## Troubleshooting (Common Issues)
Issue | Fix
------|-----
Port 5000 in use | `netstat -ano | findstr :5000` then `taskkill /PID <PID> /F`
Missing model files | Run model trainer: `python models/create_simple_working_model.py`
Build errors on Windows | Use binary wheels: `pip install --only-binary=all -r backend\requirements.txt`
Activation issues (PowerShell) | `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
Slow/failed installs | `pip install --timeout=1000 -r backend\requirements.txt`
CORS errors | Confirm `flask-cors` installed & configured

---
## Testing Categories
- ✅ Functional: correct fraud classification
- ✅ Performance: responsive inference
- ✅ Security (basic): input sanity & CORS
- ✅ Integration: end-to-end request flow
- ✅ Data/UX: charts update & history persistence

---
## Change Log (Recent)
- Unified to single `app.py` + `index.html`
- Added expanded risk vocabularies
- Implemented heuristic fallback + feature length auto-adjust
- Added reasoning output & statistics endpoint
- Cleaned legacy README duplication and added live demo link

---
**FraudCheck Pro** – Advanced, explainable fraud detection made simple.