"""
Run Project ℵω bridge translation experiments.

This experiment translates internal statements between toy formal universes
using bridge maps. It then measures preservation, loss, distortion, and
translation quality.

These results are heuristic diagnostics, not formal equivalence proofs.
"""

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.bridges.bridge_map import starter_bridge_maps
from src.bridges.distortion import (
    DistortionAnalyzer,
    rank_reports_by_distortion,
    rank_reports_by_quality,
)
from src.bridges.translator import UniverseTranslator
from src.toy_topoi.library import find_universe_by_name
from src.toy_topoi.statements import starter_statements


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
    Shortens long names for report tables.
    """

    if len(name) > width:
        return name[: width - 3] + "..."

    return name


def run_experiment() -> None:
    """
    Runs all starter bridge translations.
    """

    bridges = starter_bridge_maps()
    statements = starter_statements()

    translator = UniverseTranslator()
    distortion_analyzer = DistortionAnalyzer()

    translation_results = []

    print_section("Project ℵω Bridge Translation Engine")
    print(f"Bridge maps loaded: {len(bridges)}")
    print(f"Starter statements loaded: {len(statements)}")
    print()
    print(
        "This experiment translates statements across toy mathematical universes "
        "and measures what meaning is preserved, weakened, distorted, or lost."
    )

    print_section("Bridge Inventory")

    for bridge in bridges:
        print(bridge.describe())
        print("-" * 90)

    for bridge in bridges:
        source_universe = find_universe_by_name(bridge.source_universe_name)
        target_universe = find_universe_by_name(bridge.target_universe_name)

        if source_universe is None or target_universe is None:
            print(f"Skipping bridge because universe was not found: {bridge.name}")
            continue

        source_statements = [
            statement
            for statement in statements
            if statement.origin_universe == bridge.source_universe_name
        ]

        for statement in source_statements:
            translation_results.append(
                translator.translate(
                    statement=statement,
                    source_universe=source_universe,
                    target_universe=target_universe,
                    bridge=bridge,
                )
            )

    reports = distortion_analyzer.analyze_many(translation_results)

    print_section("Translation Summary")
    print(f"Total translations executed: {len(translation_results)}")
    print(f"Total distortion reports generated: {len(reports)}")

    status_counts = {}
    grade_counts = {}

    for result in translation_results:
        status = result.translation_status.value
        status_counts[status] = status_counts.get(status, 0) + 1

    for report in reports:
        grade = report.translation_grade.value
        grade_counts[grade] = grade_counts.get(grade, 0) + 1

    print()
    print("Translation status counts:")
    for status, count in sorted(status_counts.items()):
        print(f"- {status}: {count}")

    print()
    print("Translation grade counts:")
    for grade, count in sorted(grade_counts.items()):
        print(f"- {grade}: {count}")

    print_section("Best Translation Results")

    quality_ranked_reports = rank_reports_by_quality(reports)

    best_header = (
        f"{'Rank':<5}"
        f"{'Statement':<38}"
        f"{'Source':<42}"
        f"{'Target':<42}"
        f"{'Grade':<12}"
        f"{'Distortion':>12}"
    )

    print(best_header)
    print("-" * len(best_header))

    for index, report in enumerate(quality_ranked_reports[:10], start=1):
        print(
            f"{index:<5}"
            f"{format_name(report.statement_name, 38):<38}"
            f"{format_name(report.source_universe_name, 42):<42}"
            f"{format_name(report.target_universe_name, 42):<42}"
            f"{report.translation_grade.value:<12}"
            f"{report.overall_distortion_index:>12.2f}"
        )

    print_section("Most Distorted Translation Results")

    distortion_ranked_reports = rank_reports_by_distortion(reports)

    print(best_header)
    print("-" * len(best_header))

    for index, report in enumerate(distortion_ranked_reports[:10], start=1):
        print(
            f"{index:<5}"
            f"{format_name(report.statement_name, 38):<38}"
            f"{format_name(report.source_universe_name, 42):<42}"
            f"{format_name(report.target_universe_name, 42):<42}"
            f"{report.translation_grade.value:<12}"
            f"{report.overall_distortion_index:>12.2f}"
        )

    print_section("Detailed Translation Result Example")

    if translation_results:
        print(translation_results[0].describe())
    else:
        print("No translation results were generated.")

    print_section("Detailed Distortion Report Example")

    if reports:
        print(distortion_ranked_reports[0].describe())
    else:
        print("No distortion reports were generated.")

    print_section("Experiment Interpretation")
    print(
        "The bridge engine shows that translating a statement is not just "
        "renaming symbols. When a statement moves between universes, its truth "
        "value, proof status, required features, and semantic structure may "
        "change. The distortion analyzer makes these changes explicit. This is "
        "the first bridge layer of Project ℵω: a computational system for "
        "studying preservation and loss across toy formal universes."
    )


if __name__ == "__main__":
    run_experiment()
