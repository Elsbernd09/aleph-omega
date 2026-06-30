"""
Run Project ℵω cognitive morphism experiments.

This experiment models the path:

    informal intuition -> symbolic statement -> cognitive morphism -> gap report

The results are heuristic diagnostics. They are not claims of complete
automatic theorem formalization.
"""

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.cognitive_morphism.formalizer import InformalFormalizer
from src.cognitive_morphism.gap_analyzer import (
    FormalizationGapAnalyzer,
    rank_gap_reports_by_quality,
    rank_gap_reports_by_severity,
)
from src.cognitive_morphism.intuition import starter_intuitions


def print_section(title: str) -> None:
    """
    Prints a clean report section.
    """

    print()
    print("=" * 120)
    print(title)
    print("=" * 120)


def format_name(name: str, width: int) -> str:
    """
    Shortens long names for tables.
    """

    if len(name) > width:
        return name[: width - 3] + "..."

    return name


def run_experiment() -> None:
    """
    Runs the full cognitive morphism experiment.
    """

    intuitions = starter_intuitions()
    formalizer = InformalFormalizer()
    gap_analyzer = FormalizationGapAnalyzer()

    drafts = formalizer.formalize_many(intuitions)
    reports = gap_analyzer.analyze_many(drafts)

    print_section("Project ℵω Cognitive Morphism Layer")
    print(f"Starter intuitions loaded: {len(intuitions)}")
    print(f"Formalization drafts generated: {len(drafts)}")
    print(f"Formalization gap reports generated: {len(reports)}")
    print()
    print(
        "This experiment converts informal mathematical intuitions into starter "
        "symbolic statements, then measures what is preserved, lost, added, or "
        "distorted during formalization."
    )

    print_section("Intuition Inventory")

    for intuition in intuitions:
        print(intuition.describe())
        print("-" * 90)

    print_section("Formalization Drafts")

    for draft in drafts:
        print(draft.describe())
        print("-" * 90)

    print_section("Best Formalizations by Gap Index")

    quality_ranked = rank_gap_reports_by_quality(reports)

    header = (
        f"{'Rank':<5}"
        f"{'Intuition':<40}"
        f"{'Statement':<42}"
        f"{'Severity':<14}"
        f"{'Gap':>8}"
        f"{'Quality':>10}"
        f"{'Review':>10}"
    )

    print(header)
    print("-" * len(header))

    for index, report in enumerate(quality_ranked, start=1):
        print(
            f"{index:<5}"
            f"{format_name(report.intuition_name, 40):<40}"
            f"{format_name(report.statement_name, 42):<42}"
            f"{report.severity.value:<14}"
            f"{report.gap_index:>8.2f}"
            f"{report.formalization_quality_score:>10.2f}"
            f"{report.review_urgency_score:>10.2f}"
        )

    print_section("Largest Formalization Gaps")

    severity_ranked = rank_gap_reports_by_severity(reports)

    print(header)
    print("-" * len(header))

    for index, report in enumerate(severity_ranked, start=1):
        print(
            f"{index:<5}"
            f"{format_name(report.intuition_name, 40):<40}"
            f"{format_name(report.statement_name, 42):<42}"
            f"{report.severity.value:<14}"
            f"{report.gap_index:>8.2f}"
            f"{report.formalization_quality_score:>10.2f}"
            f"{report.review_urgency_score:>10.2f}"
        )

    print_section("Review-Needed Formalizations")

    review_needed = [
        draft for draft in drafts
        if draft.requires_review
    ]

    if not review_needed:
        print("No formalization drafts currently require review.")
    else:
        for draft in review_needed:
            print(
                f"- {draft.intuition.name} -> {draft.statement.name} "
                f"(confidence={draft.confidence}, "
                f"morphism_status={draft.morphism.status.value}, "
                f"quality={draft.morphism.formalization_quality_score()})"
            )

    print_section("Detailed Gap Report Example")

    if severity_ranked:
        print(severity_ranked[0].describe())
    else:
        print("No gap reports were generated.")

    print_section("Experiment Interpretation")
    print(
        "The cognitive morphism layer makes the informal-to-formal transition "
        "inspectable. It shows that formalization is not just symbol creation: "
        "some intuitive properties are preserved, some metaphors are lost, and "
        "some formal structure is added by the system. The formalization gap "
        "analyzer helps identify which generated statements need human review "
        "before they should be treated as serious mathematics."
    )


if __name__ == "__main__":
    run_experiment()
