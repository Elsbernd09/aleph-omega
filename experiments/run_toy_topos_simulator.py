"""
Run the Project ℵω toy topos simulator experiment.

This experiment evaluates starter mathematical statements across multiple toy
formal universes. It uses the internal language analyzer, the toy topos
simulator, and the toy subobject classifier.

The results are heuristic and educational. They are not formal proofs and do
not implement full topos theory.
"""

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.toy_topoi.library import standard_universes
from src.toy_topoi.simulator import ToyToposSimulator
from src.toy_topoi.statements import starter_statements
from src.toy_topoi.subobject_classifier import classify_simulation_results


def print_section(title: str) -> None:
    """
    Prints a clean report section divider.
    """

    print()
    print("=" * 110)
    print(title)
    print("=" * 110)


def format_name(name: str, width: int) -> str:
    """
    Formats long names for tables.
    """

    if len(name) > width:
        return name[: width - 3] + "..."

    return name


def run_experiment() -> None:
    """
    Runs the full toy topos simulator experiment.
    """

    universes = standard_universes()
    statements = starter_statements()

    simulator = ToyToposSimulator(
        universes=universes,
        statements=statements,
    )

    results = simulator.evaluate_all()
    classifications = classify_simulation_results(results)

    print_section("Project ℵω Toy Topos Simulator")
    print(f"Universes loaded: {len(universes)}")
    print(f"Starter statements loaded: {len(statements)}")
    print(f"Total statement-universe evaluations: {len(results)}")
    print()
    print(
        "Important: these evaluations are heuristic internal-language analyses, "
        "not theorem-proving results."
    )

    print_section("Statement Profiles Across Universes")

    for profile in simulator.statement_profiles():
        print(profile.describe())
        print("-" * 80)

    print_section("Top 12 Statement-Universe Fits")

    ranked_by_fit = simulator.ranked_results_by_fit()

    header = (
        f"{'Rank':<5}"
        f"{'Statement':<38}"
        f"{'Universe':<42}"
        f"{'Logic':<16}"
        f"{'Truth':<12}"
        f"{'Proof':<22}"
        f"{'Fit':>7}"
        f"{'Ambig':>8}"
        f"{'Ready':>8}"
    )

    print(header)
    print("-" * len(header))

    for index, result in enumerate(ranked_by_fit[:12], start=1):
        row = result.summary_row()

        print(
            f"{index:<5}"
            f"{format_name(str(row['statement']), 38):<38}"
            f"{format_name(str(row['universe']), 42):<42}"
            f"{str(row['logic']):<16}"
            f"{str(row['truth_value']):<12}"
            f"{str(row['proof_status']):<22}"
            f"{float(row['universe_fit_score']):>7.2f}"
            f"{float(row['ambiguity_score']):>8.2f}"
            f"{float(row['formalization_readiness']):>8.2f}"
        )

    print_section("Top 12 Most Ambiguous Evaluations")

    ranked_by_ambiguity = simulator.ranked_results_by_ambiguity()

    print(header)
    print("-" * len(header))

    for index, result in enumerate(ranked_by_ambiguity[:12], start=1):
        row = result.summary_row()

        print(
            f"{index:<5}"
            f"{format_name(str(row['statement']), 38):<38}"
            f"{format_name(str(row['universe']), 42):<42}"
            f"{str(row['logic']):<16}"
            f"{str(row['truth_value']):<12}"
            f"{str(row['proof_status']):<22}"
            f"{float(row['universe_fit_score']):>7.2f}"
            f"{float(row['ambiguity_score']):>8.2f}"
            f"{float(row['formalization_readiness']):>8.2f}"
        )

    print_section("Subobject Classifier Summary")

    status_counts = {}

    for classification in classifications:
        status = classification.classification_status.value
        status_counts[status] = status_counts.get(status, 0) + 1

    for status, count in sorted(status_counts.items()):
        print(f"{status}: {count}")

    print_section("Highest Membership Classifications")

    ranked_classifications = sorted(
        classifications,
        key=lambda classification: classification.membership_score,
        reverse=True,
    )

    class_header = (
        f"{'Rank':<5}"
        f"{'Statement':<38}"
        f"{'Universe':<42}"
        f"{'Class':<18}"
        f"{'Truth':<12}"
        f"{'Membership':>12}"
    )

    print(class_header)
    print("-" * len(class_header))

    for index, classification in enumerate(ranked_classifications[:12], start=1):
        print(
            f"{index:<5}"
            f"{format_name(classification.statement_name, 38):<38}"
            f"{format_name(classification.universe_name, 42):<42}"
            f"{classification.classification_status.value:<18}"
            f"{classification.truth_value.value:<12}"
            f"{classification.membership_score:>12.2f}"
        )

    print_section("Detailed Classification Example")

    best = ranked_classifications[0]
    print(best.describe())

    print_section("Experiment Interpretation")
    print(
        "This experiment demonstrates the first working toy topos simulator. "
        "Statements are evaluated inside multiple formal universes using an "
        "internal-language analyzer. The same statement can receive different "
        "truth values, proof statuses, ambiguity levels, and membership scores "
        "depending on the universe. The toy subobject classifier provides a "
        "simplified analogue of internal truth classification. These results "
        "are computationally useful for comparison and exploration, but they "
        "are not categorical proofs or full formalizations."
    )


if __name__ == "__main__":
    run_experiment()
