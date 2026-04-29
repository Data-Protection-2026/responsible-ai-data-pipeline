import json
from pathlib import Path

import pandas as pd
import streamlit as st


PROJECT_ROOT = Path(__file__).parent
OUTPUT_DIR = PROJECT_ROOT / "outputs"


st.set_page_config(page_title="Responsible AI Data Pipeline", layout="wide")

st.title("Responsible AI Data Quality, Privacy & Benchmark Pipeline")
st.caption("Portfolio dashboard for GenAI data strategy, privacy controls, synthetic augmentation, and benchmark readiness.")


@st.cache_data
def load_outputs():
    curated = pd.read_csv(OUTPUT_DIR / "curated_dataset.csv")
    rejected = pd.read_csv(OUTPUT_DIR / "rejected_records.csv")
    with open(OUTPUT_DIR / "benchmark_report.json", "r", encoding="utf-8") as file:
        metrics = json.load(file)
    return curated, rejected, metrics


try:
    curated_df, rejected_df, metrics = load_outputs()
except FileNotFoundError:
    from src.pipeline import run_pipeline

    st.info("Output files were missing, so the pipeline is running now...")
    run_pipeline()
    st.cache_data.clear()
    curated_df, rejected_df, metrics = load_outputs()


col1, col2, col3, col4 = st.columns(4)
col1.metric("Records Reviewed", metrics["total_records_reviewed"])
col2.metric("Approved", metrics["approved_records"])
col3.metric("Human Review", metrics["human_review_records"])
col4.metric("Rejected", metrics["rejected_records"])

col5, col6, col7, col8 = st.columns(4)
col5.metric("Readiness Score", metrics["benchmark_readiness_score"])
col6.metric("Failure Mode Coverage", f'{metrics["failure_mode_coverage"]:.0%}')
col7.metric("Language Coverage", f'{metrics["language_coverage"]:.0%}')
col8.metric("PII Detection Rate", f'{metrics["pii_detection_rate"]:.0%}')

st.divider()

left, right = st.columns(2)

with left:
    st.subheader("Quality Status")
    status_counts = curated_df["quality_status"].value_counts().reset_index()
    status_counts.columns = ["quality_status", "count"]
    st.bar_chart(status_counts, x="quality_status", y="count")

with right:
    st.subheader("Failure Mode Coverage")
    failure_counts = curated_df["failure_mode"].value_counts().reset_index()
    failure_counts.columns = ["failure_mode", "count"]
    st.bar_chart(failure_counts, x="failure_mode", y="count")

st.subheader("Curated Dataset Preview")
st.dataframe(
    curated_df[
        [
            "record_id",
            "modality",
            "language",
            "failure_mode",
            "has_pii",
            "quality_score",
            "quality_status",
            "quality_issues",
        ]
    ],
    use_container_width=True,
)

st.subheader("Rejected Records")
st.dataframe(
    rejected_df[
        [
            "record_id",
            "modality",
            "language",
            "failure_mode",
            "quality_score",
            "quality_status",
            "quality_issues",
        ]
    ],
    use_container_width=True,
)

st.subheader("Underrepresented Failure Modes")
if metrics["underrepresented_failure_modes"]:
    st.write(metrics["underrepresented_failure_modes"])
else:
    st.success("All benchmark failure modes are represented in the approved or reviewable dataset.")
