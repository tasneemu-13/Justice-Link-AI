# JusticeLink AI
## Explainable Machine Learning Judicial Analytics and Case Ranking System

JusticeLink AI is a modular, research-oriented AI/ML system designed to analyze judicial case structures, evaluate court pendency patterns, benchmark explainable case duration prediction algorithms, and prioritize active cases for procedural review using real Indian district court data (Kerala district courts pilot).

---

## 1. Project Highlights & Key Findings

- **Real Judicial Data Pilot:** Ingests and normalizes 1,284 genuine judicial case filings from the Kollam judicial district under the digital ONCourts initiative (Negotiable Instruments Act Section 138), alongside complete court discovery metadata mapping 180 court complexes across all 14 Kerala districts.
- **Duration & Survival Profiling:**
  - Completed cases resolve in a mean duration of **166.2 days** (Median: **149.5 days**, IQR: 158 days).
  - Non-parametric Kaplan-Meier survival curves model the probability of pending duration while correctly adjusting for right-censored active matters.
- **Machine Learning Benchmarks:**
  - Standardized regression suite evaluating Mean/Median baselines, OLS Linear Regression, Ridge, Lasso, Decision Trees, and Random Forests across 5-fold cross-validation.
  - **Lasso Regression** achieved the lowest generalization error (Test MAE: **63.49 days**, $R^2 = 0.343$), an error reduction of **25.5%** over baseline predictors.
- **Explainable Case Ranking:**
  - Implements an explainable procedural review queue for active pending cases ($N=1,006$) with auditable factor attributions (observed pendency days, cohort vintage, queue arrival index).
- **Interactive Multi-Tab Dashboard & REST API:**
  - Full Streamlit dashboard featuring 5 interactive modules.
  - FastAPI backend providing high-throughput REST endpoints for inference and queue audits.

---

## 2. Architecture & Directory Hierarchy

```text
JusticeLink AI/
├── data/
│   ├── raw/kerala/                      # Immutable source datasets & discovery metadata
│   └── processed/                       # Schema-validated parquet/csv modeling datasets
├── src/justicelink/
│   ├── ingestion/                       # Ingestion & discovery metadata parsing
│   ├── validation/                      # Data integrity & chronological constraint validator
│   ├── features/                        # Feature engineering & exploratory analysis scripts
│   ├── models/                          # Regression models, evaluation & feature importance
│   ├── ranking/                         # Explainable procedural case ranking engine
│   ├── api.py                           # FastAPI REST backend service
│   └── dashboard.py                     # Streamlit research dashboard
├── reports/
│   ├── figures/                         # High-res publication plots (KM curves, residuals, etc.)
│   ├── data_dictionary.md               # Complete schema specification & validation rules
│   ├── eda_report.md                    # Detailed exploratory analysis report
│   ├── model_evaluation_report.md       # Consolidated ML benchmarking report
│   └── top_100_ranking_explanations.json# Explainable ranking audit records
├── tests/                               # Automated unit & pipeline tests (Pytest)
└── README.md
```

---

## 3. How to Run the Application

### A. Run Automated Test Suite
```powershell
$env:PYTHONPATH="src"
$env:MPLCONFIGDIR="reports/figures"
pytest tests/
```

### B. Launch the Interactive Dashboard
```powershell
$env:PYTHONPATH="src"
streamlit run src/justicelink/dashboard.py
```

### C. Launch the FastAPI Backend
```powershell
$env:PYTHONPATH="src"
uvicorn justicelink.api:app --reload --port 8000
```
Interactive API docs available at `http://127.0.0.1:8000/docs`.

---

## 4. Ethical Safeguards & Research Limitations

- **Decision-Support Only:** JusticeLink AI provides statistical and case-management decision support for court administrators and researchers. It is **not** an autonomous decision-making system.
- **Non-Merit Ranking:** Case rankings represent procedural triage queues (e.g. flagging unmonitored pendency) and must never be interpreted as judicial evaluations of legal merit, guilt, or outcome predictability.
