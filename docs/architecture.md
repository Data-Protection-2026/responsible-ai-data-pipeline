# Architecture

## Pipeline layers

```text
1. Raw data intake
   - Candidate records from enterprise systems, vendors, or public-permissive sources

2. Privacy scan
   - Detects sensitive data patterns
   - Produces privacy metadata
   - Redacts downstream text fields

3. Governance validation
   - Consent status
   - License status
   - Source system
   - Collection method

4. Data quality scoring
   - Required field completeness
   - Language support
   - Modality support
   - Duplicate detection
   - Minimum text quality

5. Synthetic augmentation
   - Adds scenario-based examples for missing model failure modes
   - Supports benchmark coverage and edge-case testing

6. Benchmark coverage
   - Measures whether the dataset covers target failure modes, languages, and modalities
   - Produces readiness score

7. Reporting
   - Curated dataset
   - Rejected records
   - Benchmark report
   - Executive summary
   - Data card
```

## Design principles

- Privacy by design
- Data minimization
- Explicit consent and license controls
- Human review for uncertain cases
- Data quality as a measurable control
- Synthetic data as a gap-filling strategy
- Benchmark coverage tied to model failure modes
