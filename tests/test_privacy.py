from src.privacy import redact_text, scan_text


def test_scan_text_detects_email():
    findings = scan_text("Please contact test.user@example.com for support.")
    assert any(finding.finding_type == "email" for finding in findings)


def test_redact_text_removes_ssn():
    redacted = redact_text("Customer provided SSN 123-45-6789.")
    assert "123-45-6789" not in redacted
    assert "[REDACTED_SSN]" in redacted


def test_redact_text_removes_phone():
    redacted = redact_text("Call me at 404-555-1212 tomorrow.")
    assert "404-555-1212" not in redacted
    assert "[REDACTED_PHONE]" in redacted
