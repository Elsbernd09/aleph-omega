"""
Run the Project ℵω toy universe comparison experiment.

This experiment loads the standard toy universes, compares them pairwise,
and prints a research-style report about compatibility, distortion, and
translation difficulty.

The results are heuristic. They are not mathematical equivalence proofs.
"""

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.toy_topoi.comparator import UniverseComparator
from src.toy_topoi.connectives import ToyConnectiveAlgebra
from src.toy_topoi.library import standard_universes
from src.toy_topoi.truth_values import TruthValue


def print_section(title: str) -> None:
    """
    Prints a clean report section divider.
    """

    print()
    print("=" * 110)
    print(title)
    print("=" * 110)


def format_list(values: list[str], max_items: int = 5) -> str:
    """
    Formats a list for compact console display.
    """

    if not values:
        return "none"

    if len(values) <= max_items:
        return ", ".join(values)

    return ", ".join(values[:max_items]) + f", ... (+{len(values) - max_items} more)"


def print_universe_inventory() -> None:
    """
    Prints all standard universes and their core properties.
    """

    universes = standard_universes()

    print_section("Project ℵω Toy Logical Universe Inventory")
    print(f"Universes loaded: {len(universes)}")
    print()

    header = (
        f"{'Universe':<48}"
        f"{'Logic':<18}"
        f"{'Truth Values':<32}"
        f"{'Express':>9}"
        f"{'Stable':>9}"
    )

    print(header)
    print("-" * len(header))

    for universe in universes:
        name = universe.name[:45] + "..." if len(universe.name) > 48 else universe.name
        values = format_list(universe.truth_space.value_names(), max_items=4)

        print(
            f"{name:<48}"
            f"{universe.logic_family.value:<18}"
            f"{values:<32}"
            f"{universe.expressivity_score():>9.2f}"
            f"{universe.stability_score():>9.2f}"
        )


def print_comparison_report(top_n: int = 10) -> None:
    """
    Prints ranked pairwise universe comparisons.
    """

    universes = standard_universes()
    comparator = UniverseComparator()
    comparisons = comparator.compare_all(universes)

    ranked_high = sorted(
        comparisons,
        key=lambda comparison: comparison.compatibility_score,
        reverse=True,
    )

    ranked_low = sorted(
        comparisons,
        key=lambda comparison: comparison.compatibility_score,
    )

    print_section(f"Top {top_n} Most Compatible Universe Transports")

    header = (
        f"{'Rank':<5}"
        f"{'Source':<38}"
        f"{'Target':<38}"
        f"{'Score':>8}"
        f"{'Interpretation':<70}"
    )

    print(header)
    print("-" * len(header))

    for index, comparison in enumerate(ranked_high[:top_n], start=1):
        source = comparison.source_name[:35] + "..." if len(comparison.source_name) > 38 else comparison.source_name
        target = comparison.target_name[:35] + "..." if len(comparison.target_name) > 38 else comparison.target_name

        print(
            f"{index:<5}"
            f"{source:<38}"
            f"{target:<38}"
            f"{comparison.compatibility_score:>8.2f}"
            f"{comparison.interpretation:<70}"
        )

    print_section(f"Top {top_n} Most Difficult Universe Transports")

    print(header)
    print("-" * len(header))

    for index, comparison in enumerate(ranked_low[:top_n], start=1):
        source = comparison.source_name[:35] + "..." if len(comparison.source_name) > 38 else comparison.source_name
        target = comparison.target_name[:35] + "..." if len(comparison.target_name) > 38 else comparison.target_name

        print(
            f"{index:<5}"
            f"{source:<38}"
            f"{target:<38}"
            f"{comparison.compatibility_score:>8.2f}"
            f"{comparison.interpretation:<70}"
        )


def print_detailed_example() -> None:
    """
    Prints one detailed comparison example.
    """

    universes = standard_universes()
    comparator = UniverseComparator()

    source = next(universe for universe in universes if universe.logic_family.value == "paraconsistent")
    target = next(universe for universe in universes if universe.logic_family.value == "classical")

    comparison = comparator.compare(source, target)

    print_section("Detailed Example: Paraconsistent Universe to Classical Universe")

    print(f"Source: {comparison.source_name}")
    print(f"Target: {comparison.target_name}")
    print(f"Compatibility score: {comparison.compatibility_score}")
    print(f"Shared truth values: {format_list(comparison.shared_truth_values)}")
    print(f"Source-only truth values: {format_list(comparison.source_only_truth_values)}")
    print(f"Target-only truth values: {format_list(comparison.target_only_truth_values)}")
    print(f"Shared inference rules: {format_list(comparison.shared_inference_rules)}")
    print(f"Source-only inference rules: {format_list(comparison.source_only_inference_rules)}")
    print(f"Target-only inference rules: {format_list(comparison.target_only_inference_rules)}")
    print(f"Contradiction compatibility: {comparison.contradiction_compatibility}")
    print(f"Unknown compatibility: {comparison.unknown_compatibility}")
    print(f"Modal compatibility: {comparison.modal_compatibility}")
    print(f"Expressivity gap: {comparison.expressivity_gap}")
    print(f"Stability gap: {comparison.stability_gap}")
    print(f"Interpretation: {comparison.interpretation}")


def print_connective_examples() -> None:
    """
    Prints examples of toy connective behavior across universes.
    """

    universes = standard_universes()

    print_section("Toy Connective Behavior Examples")

    for universe in universes:
        algebra = ToyConnectiveAlgebra(universe.truth_space)

        print()
        print(f"Universe: {universe.name}")
        print(f"Logic family: {universe.logic_family.value}")

        if universe.accepts_truth_value(TruthValue.TRUE):
            negated = algebra.negate(TruthValue.TRUE)
            print(f"not true -> {negated.value.value} ({negated.explanation})")

        if (
            universe.accepts_truth_value(TruthValue.TRUE)
            and universe.accepts_truth_value(TruthValue.FALSE)
        ):
            conjunction = algebra.conjunction(TruthValue.TRUE, TruthValue.FALSE)
            implication = algebra.implication(TruthValue.TRUE, TruthValue.FALSE)

            print(f"true and false -> {conjunction.value.value} ({conjunction.explanation})")
            print(f"true implies false -> {implication.value.value} ({implication.explanation})")

        if universe.accepts_truth_value(TruthValue.BOTH):
            both_negated = algebra.negate(TruthValue.BOTH)
            print(f"not both -> {both_negated.value.value} ({both_negated.explanation})")


def run_experiment() -> None:
    """
    Runs the full universe comparison experiment.
    """

    print_universe_inventory()
    print_comparison_report(top_n=10)
    print_detailed_example()
    print_connective_examples()

    print_section("Experiment Interpretation")
    print(
        "This experiment demonstrates the first working toy universe layer of "
        "Project ℵω. The system can represent multiple logical universes, "
        "compare their truth spaces and inference rules, estimate translation "
        "compatibility, and display examples of connective behavior. These "
        "comparisons are heuristic and educational. They make differences "
        "between formal environments explicit without claiming full logical or "
        "category-theoretic equivalence."
    )


if __name__ == "__main__":
    run_experiment()
