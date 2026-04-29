# Responsible AI Data Quality, Privacy, Synthetic Data and Benchmark Pipeline

A portfolio-ready GenAI data strategy project that demonstrates how AI can turn raw enterprise data into a governed, privacy-safe, high-quality dataset for model training, fine-tuning, evaluation, and benchmark creation.

This project was designed to demonstrate the core capabilities required for AI data strategies:

- Data quality framework for AI training candidates
- Privacy and sensitive data detection with redaction
- Consent, licensing, and source governance checks
- Synthetic data generation to close coverage gaps
- Golden benchmark set creation and coverage scoring
- Data readiness reporting for executive and technical audiences
- Streamlit dashboard for portfolio demonstration

---
## Live Demo

View the deployed Streamlit dashboard here:  
https://responsible-ai-data-pipeline.streamlit.app/

## Why this project matters

Foundation models are only as strong as the data flywheel behind them. This project simulates the operating model for that flywheel:

```text
Raw data candidates
        ↓
Privacy scan + de-identification
        ↓
Data quality checks
        ↓
Consent/license validation
        ↓
Synthetic data augmentation
        ↓
Golden benchmark coverage review
        ↓
Curated training/evaluation dataset
        ↓
Executive data readiness report
```

## Portfolio story

**Business problem:**  
Enterprise teams want to reuse customer interaction data for GenAI fine-tuning and evaluation, but the data includes privacy risk, inconsistent quality, uncertain consent, vendor/license restrictions, duplicate records, and uneven benchmark coverage.

**Solution:**  
This pipeline evaluates raw data candidates, identifies privacy and quality issues, redacts sensitive information, rejects risky records, generates synthetic examples for underrepresented model failure modes, and produces a benchmark readiness score.

**Executive outcome:**  
Leaders can see which data is approved, rejected, or requires human review, which failure modes need more data, and whether the dataset is ready for GenAI use.

---

## Features

| Capability | What it demonstrates |
|---|---|
| Privacy scanning | Detects emails, phone numbers, SSNs, credit card-like numbers, and other sensitive patterns |
| Redaction | Produces privacy-safe text fields for downstream AI use |
| Consent and license checks | Rejects records that do not meet approved usage criteria |
| Data quality scoring | Scores each record using completeness, duplication, language, modality, and quality rules |
| Synthetic data generation | Creates synthetic examples to strengthen weak benchmark areas |
| Benchmark evaluation | Measures failure mode, language, and modality coverage |
| Data card generation | Produces a governance artifact explaining dataset purpose, risks, and limitations |
| Streamlit dashboard | Provides visual portfolio demonstration for recruiters and hiring managers |

---

## Project structure

```text
responsible-ai-data-pipeline/
├── README.md
├── requirements.txt
├── run_pipeline.py
├── dashboard.py
├── data/
│   ├── raw/
│   │   └── ai_training_candidates.csv
│   └── benchmark/
│       └── golden_benchmark.csv
├── src/
│   ├── benchmark.py
│   ├── pipeline.py
│   ├── privacy.py
│   ├── quality.py
│   ├── report.py
│   └── synthetic.py
├── outputs/
│   ├── curated_dataset.csv
│   ├── rejected_records.csv
│   ├── benchmark_report.json
│   ├── executive_summary.json
│   └── data_card.md
├── tests/
│   └── test_privacy.py
└── docs/
    ├── architecture.md
    ├── portfolio_talk_track.md
    └── resume_bullets.md
```

---

## How to run

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/responsible-ai-data-pipeline.git
cd responsible-ai-data-pipeline
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

```bash
# Mac/Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the pipeline

```bash
python run_pipeline.py
```

This creates updated files in the `outputs/` folder.

### 5. Launch the dashboard

```bash
streamlit run dashboard.py
```

---

## Example output

After running the pipeline, the project produces:

- `outputs/curated_dataset.csv` — approved and reviewable privacy-safe records
- `outputs/rejected_records.csv` — records rejected for privacy, consent, license, or quality risk
- `outputs/benchmark_report.json` — coverage and data readiness metrics
- `outputs/executive_summary.json` — high-level metrics for leadership
- `outputs/data_card.md` — governance artifact for dataset usage

Example readiness metrics:

```json
{
  "total_records_reviewed": 38,
  "approved_records": 27,
  "human_review_records": 7,
  "rejected_records": 4,
  "pii_detection_rate": 0.18,
  "benchmark_readiness_score": 82.5
}
```
## Business Value

This project demonstrates how organizations can evaluate whether datasets are ready for responsible GenAI use. The pipeline applies privacy checks, consent and licensing validation, data quality scoring, synthetic data augmentation, and benchmark readiness reporting before data is used for training, fine-tuning, or evaluation.

The dashboard helps technical, privacy, governance, and executive stakeholders understand whether data is approved, requires human review, or should be rejected before AI use.

---

## Disclaimer

This is a portfolio demonstration project using synthetic and sample data. It is not intended to replace enterprise-grade privacy tooling, legal review, model risk management, or production data governance platforms.
