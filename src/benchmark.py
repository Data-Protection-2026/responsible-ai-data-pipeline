from typing import Dict

import pandas as pd


def _coverage_ratio(dataset_values, benchmark_values) -> float:
    benchmark_set = set(benchmark_values)
    if not benchmark_set:
        return 0.0

    dataset_set = set(dataset_values)
    return round(len(dataset_set.intersection(benchmark_set)) / len(benchmark_set), 4)


def evaluate_benchmark(curated_df: pd.DataFrame, rejected_df: pd.DataFrame, benchmark_df: pd.DataFrame) -> Dict[str, object]:
    approved_or_review = curated_df[curated_df["quality_status"].isin(["approved", "human_review"])].copy()

    total_reviewed = int(len(curated_df) + len(rejected_df))
    approved_records = int((curated_df["quality_status"] == "approved").sum())
    review_records = int((curated_df["quality_status"] == "human_review").sum())
    rejected_records = int(len(rejected_df))

    pii_records = int(curated_df["has_pii"].sum() + rejected_df["has_pii"].sum()) if "has_pii" in rejected_df.columns else int(curated_df["has_pii"].sum())

    failure_mode_coverage = _coverage_ratio(
        approved_or_review["failure_mode"].dropna().unique(),
        benchmark_df["failure_mode"].dropna().unique(),
    )

    language_coverage = _coverage_ratio(
        approved_or_review["language"].dropna().unique(),
        benchmark_df["language"].dropna().unique(),
    )

    modality_coverage = _coverage_ratio(
        approved_or_review["modality"].dropna().unique(),
        benchmark_df["modality"].dropna().unique(),
    )

    avg_quality_score = round(float(approved_or_review["quality_score"].mean()), 2) if len(approved_or_review) else 0.0

    # Weighted score balances quality, coverage, and risk reduction.
    benchmark_readiness_score = round(
        (avg_quality_score * 0.35)
        + (failure_mode_coverage * 100 * 0.30)
        + (language_coverage * 100 * 0.15)
        + (modality_coverage * 100 * 0.10)
        + ((1 - (rejected_records / max(total_reviewed, 1))) * 100 * 0.10),
        2,
    )

    underrepresented_failure_modes = sorted(
        set(benchmark_df["failure_mode"].dropna().unique())
        - set(approved_or_review["failure_mode"].dropna().unique())
    )

    return {
        "total_records_reviewed": total_reviewed,
        "approved_records": approved_records,
        "human_review_records": review_records,
        "rejected_records": rejected_records,
        "pii_detection_rate": round(pii_records / max(total_reviewed, 1), 4),
        "average_quality_score": avg_quality_score,
        "failure_mode_coverage": failure_mode_coverage,
        "language_coverage": language_coverage,
        "modality_coverage": modality_coverage,
        "underrepresented_failure_modes": underrepresented_failure_modes,
        "benchmark_readiness_score": benchmark_readiness_score,
    }
