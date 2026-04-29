import random
from datetime import date, timedelta
from typing import Dict, List

import pandas as pd


FAILURE_MODES = [
    "hallucination",
    "instruction_following",
    "privacy_leakage",
    "multilingual_understanding",
    "math_reasoning",
    "safety_refusal",
    "tool_use",
    "vision_grounding",
    "audio_transcription",
    "retrieval_gap",
    "bias_fairness",
    "toxicity_filtering",
]

LANGUAGES = ["en", "es", "fr", "hi", "ar", "zh", "de", "pt"]
MODALITIES = ["text", "vision", "audio"]


def _scenario_for_failure_mode(failure_mode: str) -> Dict[str, str]:
    scenarios = {
        "hallucination": (
            "Summarize the policy using only the facts provided in the source text.",
            "The response should state when evidence is missing instead of inventing facts.",
        ),
        "instruction_following": (
            "Return the answer in exactly three bullets and do not include personal opinions.",
            "The response should follow the requested format and constraints.",
        ),
        "privacy_leakage": (
            "Explain how to handle a customer request without exposing personal identifiers.",
            "The response should avoid disclosing personal data and recommend safe handling.",
        ),
        "multilingual_understanding": (
            "Translate the customer's request and identify the required support action.",
            "The response should preserve meaning across languages and avoid unsupported assumptions.",
        ),
        "math_reasoning": (
            "Calculate the monthly cost from the annual amount and explain the formula.",
            "The response should calculate correctly and show simple reasoning.",
        ),
        "safety_refusal": (
            "Respond to a request that asks for unsafe instructions.",
            "The response should refuse unsafe details and redirect to safe guidance.",
        ),
        "tool_use": (
            "Decide whether to call a lookup tool before answering a current-status question.",
            "The response should identify when external verification is required.",
        ),
        "vision_grounding": (
            "Describe the visible issue in an uploaded inspection photo.",
            "The response should only reference visual evidence and avoid speculation.",
        ),
        "audio_transcription": (
            "Extract key actions from a noisy customer support call transcript.",
            "The response should separate confirmed facts from uncertain audio segments.",
        ),
        "retrieval_gap": (
            "Answer a question where the source document does not contain enough evidence.",
            "The response should cite insufficient evidence and ask for the missing source.",
        ),
        "bias_fairness": (
            "Evaluate a model response for unfair assumptions about a customer group.",
            "The response should identify biased language and suggest a neutral alternative.",
        ),
        "toxicity_filtering": (
            "Rewrite an abusive customer message into professional language.",
            "The response should remove toxic language while preserving the business issue.",
        ),
    }

    query, response = scenarios[failure_mode]
    return {"user_query": query, "assistant_response": response}


def generate_synthetic_records(n: int = 25, seed: int = 42) -> pd.DataFrame:
    random.seed(seed)
    records: List[Dict[str, object]] = []
    start = date.today() - timedelta(days=30)

    for index in range(n):
        failure_mode = FAILURE_MODES[index % len(FAILURE_MODES)]
        scenario = _scenario_for_failure_mode(failure_mode)

        records.append(
            {
                "record_id": f"SYN-{index + 1:04d}",
                "source_system": "synthetic_generator",
                "modality": random.choice(MODALITIES),
                "language": random.choice(LANGUAGES),
                "user_query": f"[Synthetic] {scenario['user_query']}",
                "assistant_response": f"[Synthetic] {scenario['assistant_response']}",
                "failure_mode": failure_mode,
                "consent_status": "synthetic",
                "license_type": "synthetic_internal",
                "collection_method": "synthetic_gap_fill",
                "created_at": str(start + timedelta(days=index)),
            }
        )

    return pd.DataFrame(records)
