"""
Run the Project ℵω Generative Axiom Engine experiment.

This script loads the starter axiom library, generates additional candidate
axioms, scores everything with the AxiomEvaluator, and prints a ranked report.

The output is experimental. Scores are heuristic research instruments, not
mathematical proofs.
"""

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.generative_axioms.evaluator import AxiomEvaluator
from src.generative_axioms.generator import AxiomGenerator
from src.generative_axioms.library import foundational_axioms


def format_score(value: float) -> str:
    """
    Formats a score for console output.
    """

    return f"{value:>5.2f}"


def print_section(title: str) -> None:
    """
    Prints a section divider.
    """

    print()
    print("=" * 100)
    print(title)
    print("=" * 100)


def run_experiment(top_n: int = 20) -> None:
    """
    Runs the axiom engine experiment.
    """

    seed_axioms = foundational_axioms()

    generator = AxiomGenerator()
    generated_axioms = generator.generate_all(seed_axioms=seed_axioms)

    all_axioms = seed_axioms + generated_axioms

    evaluator = AxiomEvaluator(reference_axioms=seed_axioms)
    ranked = evaluator.rank_axioms(all_axioms)

    print_section("Project ℵω Generative Axiom Engine")
    print(f"Seed axioms: {len(seed_axioms)}")
    print(f"Generated candidate axioms: {len(generated_axioms)}")
    print(f"Total axioms evaluated: {len(all_axioms)}")
    print()
    print("Important: These scores are heuristic. They are not mathematical proofs.")

    print_section(f"Top {top_n} Ranked Axiom Candidates")

    header = (
        f"{'Rank':<5}"
        f"{'Axiom':<45}"
        f"{'Status':<16}"
        f"{'Overall':>9}"
        f"{'Complex':>9}"
        f"{'Novel':>9}"
        f"{'Risk':>9}"
        f"{'Express':>9}"
        f"{'Stable':>9}"
    )

    print(header)
    print("-" * len(header))

    for index, (axiom, score) in enumerate(ranked[:top_n], start=1):
        name = axiom.name[:42] + "..." if len(axiom.name) > 45 else axiom.name

        print(
            f"{index:<5}"
            f"{name:<45}"
            f"{axiom.status.value:<16}"
            f"{format_score(score.overall_interest):>9}"
            f"{format_score(score.complexity):>9}"
            f"{format_score(score.novelty):>9}"
            f"{format_score(score.contradiction_risk):>9}"
            f"{format_score(score.expressivity):>9}"
            f"{format_score(score.stability):>9}"
        )

    print_section("Highest Ranked Candidate Explanation")

    best_axiom, best_score = ranked[0]

    print(best_axiom.describe())
    print()
    print("Scores:")
    for key, value in best_score.as_dict().items():
        print(f"- {key}: {value}")

    print_section("Experiment Interpretation")
    print(
        "This experiment demonstrates the first working version of the "
        "Generative Axiom Engine. The system can represent axioms as structured "
        "objects, generate additional candidates, score them, and rank them by "
        "research interest. The ranking does not prove that any axiom is true. "
        "It identifies candidates that may be useful for later toy-universe, "
        "bridge-transport, or formalization experiments."
    )


if __name__ == "__main__":
    run_experiment()
