# AI Training Candidate Dataset Card

Generated: 2026-04-29T15:08:26.068222Z

## Intended use

This dataset is intended for portfolio demonstration of a governed GenAI data pipeline. It shows how raw data candidates can be evaluated for privacy, consent, licensing, quality, synthetic augmentation, and benchmark readiness before downstream AI use.

## Not intended for

- Production model training
- Legal determination of data usage rights
- Replacement of enterprise privacy engineering tools
- Use with real customer personal information

## Dataset composition

- Total records reviewed: 38
- Approved records: 22
- Human review records: 14
- Rejected records: 2
- Average quality score: 91.11
- Benchmark readiness score: 93.86

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

email, phone, ssn

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
