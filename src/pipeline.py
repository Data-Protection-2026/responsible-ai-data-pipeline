import json
from pathlib import Path
from typing import Dict

import pandas as pd

from src.benchmark import evaluate_benchmark
from src.privacy import redact_text, scan_record_text
from src.quality import apply_quality_checks, validate_schema
from src.report import write_data_card
from src.synthetic import generate_synthetic_records


def _privacy_enrich(df: pd.DataFrame) -> pd.DataFrame:
    enriched = df.copy()

    privacy_results = enriched.apply(
        lambda row: scan_record_text(row.get("user_query", ""), row.get("assistant_response", "")),
        axis=1,
    )

    privacy_df = pd.DataFrame(privacy_results.tolist())

    enriched["redacted_user_query"] = enriched["user_query"].apply(redact_text)
    enriched["redacted_assistant_response"] = enriched["assistant_response"].apply(redact_text)

    return pd.concat([enriched.reset_index(drop=True), privacy_df.reset_index(drop=True)], axis=1)


def _safe_to_json(value):
    if hasattr(value, "item"):
        return value.item()
    return value


def run_pipeline(raw_path: Path, benchmark_path: Path, output_dir: Path, synthetic_records: int = 18) -> Dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)

    raw_df = pd.read_csv(raw_path)
    benchmark_df = pd.read_csv(benchmark_path)

    missing_columns = validate_schema(raw_df)
    if missing_columns:
        raise ValueError(f"Raw dataset is missing required columns: {missing_columns}")

    synthetic_df = generate_synthetic_records(n=synthetic_records)

    combined_df = pd.concat([raw_df, synthetic_df], ignore_index=True)

    privacy_df = _privacy_enrich(combined_df)
    quality_df = apply_quality_checks(privacy_df)

    rejected_df = quality_df[quality_df["quality_status"] == "rejected"].copy()
    curated_df = quality_df[quality_df["quality_status"].isin(["approved", "human_review"])].copy()

    curated_export_columns = [
        "record_id",
        "source_system",
        "modality",
        "language",
        "redacted_user_query",
        "redacted_assistant_response",
        "failure_mode",
        "consent_status",
        "license_type",
        "collection_method",
        "created_at",
        "has_pii",
        "pii_types",
        "pii_count",
        "quality_score",
        "quality_status",
        "quality_issues",
        "content_hash",
    ]

    rejected_export_columns = curated_export_columns + ["user_query", "assistant_response"]

    curated_df[curated_export_columns].to_csv(output_dir / "curated_dataset.csv", index=False)
    rejected_df[[column for column in rejected_export_columns if column in rejected_df.columns]].to_csv(
        output_dir / "rejected_records.csv",
        index=False,
    )

    metrics = evaluate_benchmark(curated_df, rejected_df, benchmark_df)

    with (output_dir / "benchmark_report.json").open("w", encoding="utf-8") as file:
        json.dump(metrics, file, indent=2, default=_safe_to_json)

    executive_summary = {
        "total_records_reviewed": metrics["total_records_reviewed"],
        "approved_records": metrics["approved_records"],
        "human_review_records": metrics["human_review_records"],
        "rejected_records": metrics["rejected_records"],
        "pii_detection_rate": metrics["pii_detection_rate"],
        "benchmark_readiness_score": metrics["benchmark_readiness_score"],
        "recommended_decision": (
            "Proceed with controlled pilot"
            if metrics["benchmark_readiness_score"] >= 80
            else "Remediate data gaps before pilot"
        ),
    }

    with (output_dir / "executive_summary.json").open("w", encoding="utf-8") as file:
        json.dump(executive_summary, file, indent=2, default=_safe_to_json)

    write_data_card(curated_df, rejected_df, metrics, output_dir / "data_card.md")

    return executive_summary
