# Portfolio Talk Track

## 30-second version

I built a Responsible AI data pipeline that shows how raw enterprise data can be evaluated before it is used for GenAI. The pipeline scans for sensitive data, redacts privacy risk, validates consent and licensing, scores data quality, generates synthetic examples for weak coverage areas, and measures readiness against a golden benchmark set.

## 2-minute version

The business problem is that companies want to use enterprise data for GenAI, but that data often contains privacy risk, unclear usage rights, duplicates, inconsistent quality, and incomplete coverage across model failure modes. I designed this project as a data strategy operating model. It takes raw candidate records, applies privacy scanning and redaction, validates consent and licensing, calculates data quality scores, generates synthetic data to fill gaps, and then evaluates the resulting dataset against a benchmark file.

The output includes a curated dataset, rejected records, executive metrics, a benchmark readiness report, and a data card. This shows how I would partner with AI research, legal, privacy, security, data engineering, and business stakeholders to create a data flywheel that is safe, measurable, and useful for GenAI.

## How to explain the data flywheel

1. Model or business gaps identify where the model is weak.
2. Those gaps become data requirements.
3. Data candidates are collected from approved sources.
4. Privacy, consent, quality, and licensing controls are applied.
5. Synthetic data fills rare or risky edge cases.
6. A benchmark set measures readiness.
7. Results inform the next data collection cycle.
