"""
Generate the full Project ℵω research report.

This experiment runs the meta-theory system, exports reportable artifacts,
generates a Markdown report, and saves it into the reports folder.

The generated report is a research-system summary, not a proof of new
mathematics.
"""

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from experiments.run_meta_theory_report import (
    build_axiom_scores,
    build_bridge_outputs,
    build_cognitive_outputs,
    build_universe_outputs,
)
from src.meta_theory.evaluator import GlobalEvaluationInputs, GlobalResearchEvaluator
from src.meta_theory.report import IntelligenceReportGenerator
from src.reporting.markdown_generator import MarkdownReportGenerator
from src.reporting.summary_exporter import SystemSummaryExporter


def print_section(title: str) -> None:
    """
    Prints a clean section divider.
    """

    print()
    print("=" * 120)
    print(title)
    print("=" * 120)


def build_global_inputs() -> GlobalEvaluationInputs:
    """
    Builds all global inputs for the final report.
    """

    axiom_scores = build_axiom_scores()
    universe_comparisons, simulation_results = build_universe_outputs()
    distortion_reports = build_bridge_outputs()
    gap_reports, formalization_plans = build_cognitive_outputs()

    return GlobalEvaluationInputs(
        axiom_scores=axiom_scores,
        universe_comparisons=universe_comparisons,
        simulation_results=simulation_results,
        distortion_reports=distortion_reports,
        gap_reports=gap_reports,
        formalization_plans=formalization_plans,
        metadata={
            "experiment": "run_full_project_report",
        },
    )


def run_experiment() -> None:
    """
    Runs the full report generation pipeline.
    """

    print_section("Project ℵω Full Research Report Generator")

    output_path = PROJECT_ROOT / "reports" / "project_aleph_omega_report.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print("Building global system inputs...")
    inputs = build_global_inputs()

    print("Evaluating global system metrics...")
    evaluator = GlobalResearchEvaluator()
    metric_bundle = evaluator.evaluate(inputs)

    print("Generating intelligence report...")
    intelligence_report_generator = IntelligenceReportGenerator()
    intelligence_report = intelligence_report_generator.generate(metric_bundle)

    print("Exporting research artifacts...")
    exporter = SystemSummaryExporter()
    export_summary = exporter.export(
        metric_bundle=metric_bundle,
        intelligence_report=intelligence_report,
    )

    print("Generating Markdown report...")
    markdown_generator = MarkdownReportGenerator()
    markdown_report = markdown_generator.generate(
        collection=export_summary.collection,
        title="Project ℵω: Unified Research Report",
    )

    markdown_generator.save(
        report=markdown_report,
        output_path=str(output_path),
    )

    print_section("Report Generation Summary")
    print(export_summary.describe())
    print()
    print(markdown_report.describe())
    print()
    print(f"Saved report to: {output_path}")

    print_section("Interpretation")
    print(
        "The generated Markdown report summarizes Project ℵω as a computational "
        "research framework. It organizes system artifacts, metrics, limitations, "
        "review requirements, and next steps. It should not be presented as a "
        "completed proof or solved mathematical theory."
    )


if __name__ == "__main__":
    run_experiment()
