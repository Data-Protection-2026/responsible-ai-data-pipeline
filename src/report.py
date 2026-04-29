from datetime import datetime
from pathlib import Path
from typing import Dict

import pandas as pd


def write_data_card(curated_df: pd.DataFrame, rejected_df: pd.DataFrame, metrics: Dict[str, object], output_path: Path) -> None:
    pii_types = sorted(
        {
            item
            for values in curated_df.get("pii_types", pd.Series(dtype=str)).dropna().astype(str)
            for item in values.replace("[", "").replace("]", "").replace("'", "").split(", ")
            if item and item != "[]"
        }
    )

    content = f"""# AI Training Candidate Dataset Card

Generated: {datetime.utcnow().isoformat()}Z

## Intended use

This dataset is intended for portfolio demonstration of a governed GenAI data pipeline. It shows how raw data candidates can be evaluated for privacy, consent, licensing, quality, synthetic augmentation, and benchmark readiness before downstream AI use.

## Not intended for

- Production model training
- Legal determination of data usage rights
- Replacement of enterprise privacy engineering tools
- Use with real customer personal information

## Dataset composition

- Total records reviewed: {metrics["total_records_reviewed"]}
- Approved records: {metrics["approved_records"]}
- Human review records: {metrics["human_review_records"]}
- Rejected records: {metrics["rejected_records"]}
- Average quality score: {metrics["average_quality_score"]}
- Benchmark readiness score: {metrics["benchmark_readiness_score"]}

## Governance controls demonstrated

1. Schema validation
2. Consent and license validation
3. Privacy scanning
4. Text redaction
5. Duplicate detection
6. Quality scoring
7. Synthetic data augmentation
8. Benchmark coverage scoring

## Privacy findings

Detected sensitive data categories:

{", ".join(pii_types) if pii_types else "No sensitive data patterns detected in approved dataset."}

All supported sensitive data patterns are redacted in the downstream curated text fields.

## Known limitations

- Regex privacy detection is not a replacement for full enterprise DLP or privacy engineering tools.
- Synthetic records are scenario-based and should be reviewed before model use.
- Bias, toxicity, and safety scoring are represented as framework checks, not as full model-based classifiers.
- Licensing and consent rules are simplified for portfolio demonstration.

## Recommended next steps

- Add enterprise DLP integration.
- Add human review workflow with reviewer attribution.
- Add model-based toxicity and bias scoring.
- Add dataset versioning with DVC or LakeFS.
- Add labeling platform integration such as Label Studio, Labelbox, or Scale AI.
"""

    output_path.write_text(content, encoding="utf-8")
