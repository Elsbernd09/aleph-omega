"""
Run the Project ℵω meta-theory intelligence report.

This experiment evaluates the whole architecture:
- generative axiom engine,
- toy logical universe simulator,
- bridge translation engine,
- cognitive morphism layer,
- neural-symbolic formalization layer.

The output is a system intelligence report, not a mathematical proof.
"""

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.bridges.bridge_map import starter_bridge_maps
from src.bridges.distortion import DistortionAnalyzer
from src.bridges.translator import UniverseTranslator
from src.cognitive_morphism.formalization_planner import FormalizationPlanner
from src.cognitive_morphism.formalization_target import FormalizationTargetBuilder
from src.cognitive_morphism.formalizer import InformalFormalizer
from src.cognitive_morphism.gap_analyzer import FormalizationGapAnalyzer
from src.cognitive_morphism.intuition import starter_intuitions
from src.cognitive_morphism.lean_sketch import LeanSketchGenerator
from src.cognitive_morphism.proof_obligation import ProofObligationAnalyzer
from src.generative_axioms.evaluator import AxiomEvaluator
from src.generative_axioms.generator import AxiomGenerator
from src.generative_axioms.library import foundational_axioms
from src.meta_theory.evaluator import GlobalEvaluationInputs, GlobalResearchEvaluator
from src.meta_theory.report import IntelligenceReportGenerator
from src.toy_topoi.comparator import UniverseComparator
from src.toy_topoi.library import find_universe_by_name, standard_universes
from src.toy_topoi.simulator import ToyToposSimulator
from src.toy_topoi.statements import starter_statements


def print_section(title: str) -> None:
    """
    Prints a clean report section.
    """

    print()
    print("=" * 120)
    print(title)
    print("=" * 120)


def build_axiom_scores():
    """
    Builds axiom scores from seed and generated axioms.
    """

    seed_axioms = foundational_axioms()
    generator = AxiomGenerator()
    evaluator = AxiomEvaluator()

    generated_axioms = []
    all_axioms = seed_axioms + generated_axioms

    return [evaluator.score(axiom) for axiom in all_axioms]


def build_universe_outputs():
    """
    Builds universe comparisons and toy simulation results.
    """

    universes = standard_universes()
    comparator = UniverseComparator()

    universe_comparisons = comparator.compare_all(universes)

    simulator = ToyToposSimulator(
        universes=universes,
        statements=starter_statements(),
    )

    simulation_results = simulator.evaluate_all()

    return universe_comparisons, simulation_results


def build_bridge_outputs():
    """
    Builds bridge translation distortion reports.
    """

    translator = UniverseTranslator()
    distortion_analyzer = DistortionAnalyzer()

    translation_results = []

    for bridge in starter_bridge_maps():
        source_universe = find_universe_by_name(bridge.source_universe_name)
        target_universe = find_universe_by_name(bridge.target_universe_name)

        if source_universe is None or target_universe is None:
            continue

        for statement in starter_statements():
            if statement.origin_universe == bridge.source_universe_name:
                translation_results.append(
                    translator.translate(
                        statement=statement,
                        source_universe=source_universe,
                        target_universe=target_universe,
                        bridge=bridge,
                    )
                )

    return distortion_analyzer.analyze_many(translation_results)


def build_cognitive_outputs():
    """
    Builds cognitive gap reports and formalization plans.
    """

    formalizer = InformalFormalizer()
    gap_analyzer = FormalizationGapAnalyzer()
    target_builder = FormalizationTargetBuilder()
    sketch_generator = LeanSketchGenerator()
    obligation_analyzer = ProofObligationAnalyzer()
    planner = FormalizationPlanner()

    drafts = formalizer.formalize_many(starter_intuitions())
    gap_reports = gap_analyzer.analyze_many(drafts)

    targets = target_builder.build_many([draft.statement for draft in drafts])
    sketches = sketch_generator.generate_many(targets)
    obligation_reports = obligation_analyzer.analyze_many(sketches)
    formalization_plans = planner.plan_many(targets, sketches, obligation_reports)

    return gap_reports, formalization_plans


def run_experiment() -> None:
    """
    Runs the full meta-theory experiment.
    """

    print_section("Project ℵω Meta-Theory Intelligence Experiment")
    print("Building global research artifacts...")

    axiom_scores = build_axiom_scores()
    universe_comparisons, simulation_results = build_universe_outputs()
    distortion_reports = build_bridge_outputs()
    gap_reports, formalization_plans = build_cognitive_outputs()

    inputs = GlobalEvaluationInputs(
        axiom_scores=axiom_scores,
        universe_comparisons=universe_comparisons,
        simulation_results=simulation_results,
        distortion_reports=distortion_reports,
        gap_reports=gap_reports,
        formalization_plans=formalization_plans,
        metadata={
            "experiment": "run_meta_theory_report",
        },
    )

    evaluator = GlobalResearchEvaluator()
    report_generator = IntelligenceReportGenerator()

    metric_bundle = evaluator.evaluate(inputs)
    intelligence_report = report_generator.generate(metric_bundle)

    print_section("Artifact Counts")
    print(f"Axiom scores: {len(axiom_scores)}")
    print(f"Universe comparisons: {len(universe_comparisons)}")
    print(f"Toy topos simulation results: {len(simulation_results)}")
    print(f"Bridge distortion reports: {len(distortion_reports)}")
    print(f"Formalization gap reports: {len(gap_reports)}")
    print(f"Formalization plans: {len(formalization_plans)}")
    print(f"Total artifacts evaluated: {inputs.total_items()}")

    print_section("System Metric Bundle")
    print(metric_bundle.describe())

    print_section("Final Intelligence Report")
    print(intelligence_report.describe())

    print_section("Experiment Interpretation")
    print(
        "The meta-theory layer gives Project ℵω a system-level intelligence "
        "view. It does not prove new mathematics. Instead, it evaluates the "
        "architecture itself: which layers are strong, which layers are weak, "
        "where translation or formalization risk appears, and what the next "
        "research actions should be."
    )


if __name__ == "__main__":
    run_experiment()
