"""
Run Project ℵω neural-symbolic formalization experiments.

This experiment models the pipeline:

    informal intuition
    -> generated symbolic statement
    -> formalization target
    -> Lean-style sketch
    -> proof obligation report
    -> formalization plan

The output is a roadmap for formalization, not a completed proof.
"""

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.cognitive_morphism.formalization_planner import (
    FormalizationPlanner,
    rank_plans_by_burden,
    rank_plans_by_readiness,
)
from src.cognitive_morphism.formalization_target import FormalizationTargetBuilder
from src.cognitive_morphism.formalizer import InformalFormalizer
from src.cognitive_morphism.intuition import starter_intuitions
from src.cognitive_morphism.lean_sketch import LeanSketchGenerator
from src.cognitive_morphism.proof_obligation import (
    ProofObligationAnalyzer,
    rank_obligation_reports_by_burden,
    rank_obligation_reports_by_readiness,
)


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
    Runs the full neural-symbolic formalization experiment.
    """

    intuitions = starter_intuitions()

    formalizer = InformalFormalizer()
    target_builder = FormalizationTargetBuilder()
    sketch_generator = LeanSketchGenerator()
    obligation_analyzer = ProofObligationAnalyzer()
    planner = FormalizationPlanner()

    drafts = formalizer.formalize_many(intuitions)
    statements = [draft.statement for draft in drafts]
    targets = target_builder.build_many(statements)
    sketches = sketch_generator.generate_many(targets)
    obligation_reports = obligation_analyzer.analyze_many(sketches)
    plans = planner.plan_many(targets, sketches, obligation_reports)

    print_section("Project ℵω Neural-Symbolic Formalization Layer")
    print(f"Starter intuitions loaded: {len(intuitions)}")
    print(f"Formalization drafts generated: {len(drafts)}")
    print(f"Formalization targets built: {len(targets)}")
    print(f"Lean-style sketches generated: {len(sketches)}")
    print(f"Proof obligation reports generated: {len(obligation_reports)}")
    print(f"Formalization plans generated: {len(plans)}")
    print()
    print(
        "This experiment creates a formalization roadmap. It does not claim "
        "that any theorem has been proven or machine-checked."
    )

    print_section("Formalization Targets")

    target_header = (
        f"{'Rank':<5}"
        f"{'Statement':<42}"
        f"{'Target':<20}"
        f"{'Difficulty':<22}"
        f"{'Readiness':<24}"
        f"{'Work':>8}"
    )

    print(target_header)
    print("-" * len(target_header))

    for index, target in enumerate(targets, start=1):
        print(
            f"{index:<5}"
            f"{format_name(target.statement.name, 42):<42}"
            f"{target.target_kind.value:<20}"
            f"{target.difficulty.value:<22}"
            f"{target.readiness.value:<24}"
            f"{target.estimated_work_score():>8.2f}"
        )

    print_section("Lean Sketch Summary")

    sketch_header = (
        f"{'Rank':<5}"
        f"{'Statement':<42}"
        f"{'Status':<24}"
        f"{'Lines':>8}"
        f"{'Sorries':>8}"
        f"{'Machine Checked?':>18}"
    )

    print(sketch_header)
    print("-" * len(sketch_header))

    for index, sketch in enumerate(sketches, start=1):
        print(
            f"{index:<5}"
            f"{format_name(sketch.target.statement.name, 42):<42}"
            f"{sketch.status.value:<24}"
            f"{sketch.line_count():>8}"
            f"{sketch.sorry_count:>8}"
            f"{str(sketch.is_machine_checked_claim()):>18}"
        )

    print_section("Highest Proof Burdens")

    burden_ranked_reports = rank_obligation_reports_by_burden(obligation_reports)

    obligation_header = (
        f"{'Rank':<5}"
        f"{'Statement':<42}"
        f"{'Obligations':>12}"
        f"{'Blocking':>10}"
        f"{'Avg Severity':>14}"
        f"{'Index':>8}"
    )

    print(obligation_header)
    print("-" * len(obligation_header))

    for index, report in enumerate(burden_ranked_reports, start=1):
        print(
            f"{index:<5}"
            f"{format_name(report.sketch.target.statement.name, 42):<42}"
            f"{report.obligation_count():>12}"
            f"{report.blocking_count():>10}"
            f"{report.average_severity_score():>14.2f}"
            f"{report.obligation_index():>8.2f}"
        )

    print_section("Lowest Proof Burdens")

    readiness_ranked_reports = rank_obligation_reports_by_readiness(obligation_reports)

    print(obligation_header)
    print("-" * len(obligation_header))

    for index, report in enumerate(readiness_ranked_reports, start=1):
        print(
            f"{index:<5}"
            f"{format_name(report.sketch.target.statement.name, 42):<42}"
            f"{report.obligation_count():>12}"
            f"{report.blocking_count():>10}"
            f"{report.average_severity_score():>14.2f}"
            f"{report.obligation_index():>8.2f}"
        )

    print_section("Formalization Plans by Burden")

    burden_ranked_plans = rank_plans_by_burden(plans)

    plan_header = (
        f"{'Rank':<5}"
        f"{'Statement':<42}"
        f"{'Readiness Grade':<28}"
        f"{'Steps':>8}"
        f"{'Urgent':>8}"
        f"{'Burden':>8}"
    )

    print(plan_header)
    print("-" * len(plan_header))

    for index, plan in enumerate(burden_ranked_plans, start=1):
        print(
            f"{index:<5}"
            f"{format_name(plan.target.statement.name, 42):<42}"
            f"{plan.readiness_grade.value:<28}"
            f"{plan.step_count():>8}"
            f"{plan.urgent_step_count():>8}"
            f"{plan.plan_burden_score():>8.2f}"
        )

    print_section("Formalization Plans by Readiness")

    readiness_ranked_plans = rank_plans_by_readiness(plans)

    print(plan_header)
    print("-" * len(plan_header))

    for index, plan in enumerate(readiness_ranked_plans, start=1):
        print(
            f"{index:<5}"
            f"{format_name(plan.target.statement.name, 42):<42}"
            f"{plan.readiness_grade.value:<28}"
            f"{plan.step_count():>8}"
            f"{plan.urgent_step_count():>8}"
            f"{plan.plan_burden_score():>8.2f}"
        )

    print_section("Detailed Lean Sketch Example")

    if sketches:
        print(sketches[0].describe())
    else:
        print("No sketches generated.")

    print_section("Detailed Proof Obligation Example")

    if burden_ranked_reports:
        print(burden_ranked_reports[0].describe())
    else:
        print("No obligation reports generated.")

    print_section("Detailed Formalization Plan Example")

    if burden_ranked_plans:
        print(burden_ranked_plans[0].describe())
    else:
        print("No plans generated.")

    print_section("Experiment Interpretation")
    print(
        "The neural-symbolic formalization layer turns informal mathematical "
        "ideas into formalization targets, Lean-style sketches, proof obligation "
        "reports, and ordered action plans. The system is honest about unfinished "
        "work: sketches with `sorry` are not completed proofs, and statements "
        "requiring custom semantics are marked as needing review or semantic "
        "encoding. This phase makes the project more serious by separating "
        "mathematical ambition from formal proof completion."
    )


if __name__ == "__main__":
    run_experiment()
