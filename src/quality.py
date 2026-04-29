import hashlib
from typing import Dict, List

import pandas as pd


REQUIRED_COLUMNS = [
    "record_id",
    "source_system",
    "modality",
    "language",
    "user_query",
    "assistant_response",
    "failure_mode",
    "consent_status",
    "license_type",
    "collection_method",
    "created_at",
]

SUPPORTED_MODALITIES = {"text", "vision", "audio"}
SUPPORTED_LANGUAGES = {"en", "es", "fr", "hi", "ar", "zh", "de", "pt"}
APPROVED_CONSENT = {"approved", "synthetic", "public_allowed"}
APPROVED_LICENSES = {"internal_approved", "synthetic_internal", "public_permissive", "licensed_vendor"}


def content_hash(user_query: str, assistant_response: str) -> str:
    value = f"{user_query or ''}||{assistant_response or ''}".lower().strip()
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def validate_schema(df: pd.DataFrame) -> List[str]:
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    return missing_columns


def score_record(row: pd.Series, duplicate_hashes: set) -> Dict[str, object]:
    issues: List[str] = []
    score = 100

    for column in REQUIRED_COLUMNS:
        value = row.get(column)
        if pd.isna(value) or str(value).strip() == "":
            issues.append(f"missing_{column}")
            score -= 10

    if row.get("modality") not in SUPPORTED_MODALITIES:
        issues.append("unsupported_modality")
        score -= 10

    if row.get("language") not in SUPPORTED_LANGUAGES:
        issues.append("unsupported_language")
        score -= 8

    if row.get("consent_status") not in APPROVED_CONSENT:
        issues.append("consent_not_approved")
        score -= 30

    if row.get("license_type") not in APPROVED_LICENSES:
        issues.append("license_not_approved")
        score -= 30

    query = str(row.get("user_query", "") or "")
    response = str(row.get("assistant_response", "") or "")

    if len(query) < 20:
        issues.append("query_too_short")
        score -= 5

    if len(response) < 20:
        issues.append("response_too_short")
        score -= 5

    if row.get("content_hash") in duplicate_hashes:
        issues.append("duplicate_candidate")
        score -= 20

    if bool(row.get("has_pii")):
        issues.append("pii_detected_redaction_required")
        score -= 15

    score = max(score, 0)

    if score >= 85 and not any(issue in issues for issue in ["consent_not_approved", "license_not_approved"]):
        status = "approved"
    elif score >= 65 and not any(issue in issues for issue in ["consent_not_approved", "license_not_approved"]):
        status = "human_review"
    else:
        status = "rejected"

    return {
        "quality_score": score,
        "quality_status": status,
        "quality_issues": ";".join(issues) if issues else "none",
    }


def apply_quality_checks(df: pd.DataFrame) -> pd.DataFrame:
    working = df.copy()

    working["content_hash"] = working.apply(
        lambda row: content_hash(row.get("user_query"), row.get("assistant_response")),
        axis=1,
    )

    duplicated_hashes = set(
        working.loc[working.duplicated("content_hash", keep=False), "content_hash"].tolist()
    )

    scored_rows = working.apply(lambda row: score_record(row, duplicated_hashes), axis=1)
    scored_df = pd.DataFrame(scored_rows.tolist())

    return pd.concat([working.reset_index(drop=True), scored_df.reset_index(drop=True)], axis=1)
