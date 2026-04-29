from pathlib import Path

from src.pipeline import run_pipeline


if __name__ == "__main__":
    project_root = Path(__file__).parent

    summary = run_pipeline(
        raw_path=project_root / "data" / "raw" / "ai_training_candidates.csv",
        benchmark_path=project_root / "data" / "benchmark" / "golden_benchmark.csv",
        output_dir=project_root / "outputs",
        synthetic_records=18,
    )

    print("\nResponsible AI Data Pipeline completed.")
    print("Executive summary:")
    for key, value in summary.items():
        print(f"- {key}: {value}")
