import re
from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class PrivacyFinding:
    finding_type: str
    matched_text: str


PII_PATTERNS: Dict[str, re.Pattern] = {
    "email": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
    "phone": re.compile(r"\b(?:\+?1[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?)\d{3}[-.\s]?\d{4}\b"),
    "ssn": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "credit_card_like": re.compile(r"\b(?:\d[ -]*?){13,16}\b"),
    "date_of_birth_phrase": re.compile(r"\b(?:DOB|date of birth)\s*[:\-]?\s*\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b", re.IGNORECASE),
}


REDACTION_TOKENS = {
    "email": "[REDACTED_EMAIL]",
    "phone": "[REDACTED_PHONE]",
    "ssn": "[REDACTED_SSN]",
    "credit_card_like": "[REDACTED_CARD]",
    "date_of_birth_phrase": "[REDACTED_DOB]",
}


def scan_text(text: str) -> List[PrivacyFinding]:
    """Return privacy findings detected in a text field."""
    if not isinstance(text, str) or not text:
        return []

    findings: List[PrivacyFinding] = []
    for finding_type, pattern in PII_PATTERNS.items():
        for match in pattern.findall(text):
            findings.append(PrivacyFinding(finding_type=finding_type, matched_text=str(match)))
    return findings


def redact_text(text: str) -> str:
    """Redact supported sensitive data patterns from text."""
    if not isinstance(text, str) or not text:
        return text

    redacted = text
    for finding_type, pattern in PII_PATTERNS.items():
        redacted = pattern.sub(REDACTION_TOKENS[finding_type], redacted)

    return redacted


def scan_record_text(*text_fields: str) -> Dict[str, object]:
    """Scan one or more text fields and return a summarized privacy result."""
    findings: List[PrivacyFinding] = []

    for text in text_fields:
        findings.extend(scan_text(text))

    finding_types = sorted({finding.finding_type for finding in findings})

    return {
        "has_pii": bool(findings),
        "pii_types": finding_types,
        "pii_count": len(findings),
    }
