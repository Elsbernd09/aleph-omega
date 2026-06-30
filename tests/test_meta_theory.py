"""
Unit tests for Project ℵω meta-theory intelligence layer.

These tests verify that Phase 8 can:
- score system metrics,
- evaluate global research artifacts,
- generate intelligence reports,
- run the full meta-theory pipeline.
"""

from src.bridges.bridge_map import starter_bridge_maps
from src.bridges.distortion import DistortionAnalyzer, DistortionReport
from src.bridges.translator import UniverseTranslator
from src.cognitive_morphism.formalization_planner import (
    FormalizationPlan,
    FormalizationPlanner,
)
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
from src.meta_theory.metrics import (
    MetricScore,
    ResearchRiskLevel,
    SystemHealthGrade,
    SystemMetricBundle,
    grade_from_score,
    risk_from_review_pressure,
    weighted_overall_score,
)
from src.meta_theory.report import (
    IntelligenceReport,
    IntelligenceReportGenerator,
    ReportFinding,
    ReportPriority,
)
from src.toy_topoi.comparator import UniverseComparator
from src.toy_topoi.library import find_universe_by_name, standard_universes
from src.toy_topoi.simulator import ToyToposSimulator
from src.toy_topoi.statements import starter_statements


def build_test_inputs():
    seed_axioms = foundational_axioms()
    axiom_generator = AxiomGenerator()
    axiom_evaluator = AxiomEvaluator()

    generated_axioms = []
    from types import SimpleNamespace

    axiom_scores = [
        SimpleNamespace(
            overall_interest=7.0,
            stability=7.0,
            expressivity=7.0,
        )
        for axiom in seed_axioms + generated_axioms
    ]

    universes = standard_universes()
    comparator = UniverseComparator()
    universe_comparisons = comparator.compare_all(universes)

    simulator = ToyToposSimulator(
        universes=universes,
        statements=starter_statements(),
    )
    simulation_results = simulator.evaluate_all()

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

    distortion_reports = distortion_analyzer.analyze_many(translation_results)

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

    return GlobalEvaluationInputs(
        axiom_scores=axiom_scores,
        universe_comparisons=universe_comparisons,
        simulation_results=simulation_results,
        distortion_reports=distortion_reports,
        gap_reports=gap_reports,
        formalization_plans=formalization_plans,
    )


def test_grade_from_score():
    assert grade_from_score(9.0) == SystemHealthGrade.EXCELLENT
    assert grade_from_score(7.5) == SystemHealthGrade.STRONG
    assert grade_from_score(5.5) == SystemHealthGrade.DEVELOPING
    assert grade_from_score(3.5) == SystemHealthGrade.WEAK
    assert grade_from_score(1.0) == SystemHealthGrade.CRITICAL


def test_risk_from_review_pressure():
    assert risk_from_review_pressure(0, 0, 0) == ResearchRiskLevel.LOW
    assert risk_from_review_pressure(3, 0, 0) == ResearchRiskLevel.MEDIUM
    assert risk_from_review_pressure(2, 2, 0) == ResearchRiskLevel.HIGH
    assert risk_from_review_pressure(4, 2, 2) == ResearchRiskLevel.EXTREME


def test_weighted_overall_score():
    score = weighted_overall_score(
        axiom_score=8.0,
        universe_score=7.0,
        bridge_score=6.0,
        cognitive_score=7.5,
        formalization_score=5.0,
    )

    assert 0.0 <= score <= 10.0


def test_metric_score_model():
    metric = MetricScore(
        name="Test Metric",
        value=12.0,
        grade=SystemHealthGrade.EXCELLENT,
        explanation="Testing metric normalization.",
    )

    assert metric.normalized_value() == 10.0
    assert "Test Metric" in metric.describe()


def test_global_evaluation_inputs_count():
    inputs = build_test_inputs()

    assert inputs.total_items() > 0
    assert len(inputs.axiom_scores) > 0
    assert len(inputs.universe_comparisons) > 0
    assert len(inputs.simulation_results) > 0
    assert all(isinstance(report, DistortionReport) for report in inputs.distortion_reports)
    assert all(isinstance(plan, FormalizationPlan) for plan in inputs.formalization_plans)


def test_global_research_evaluator_returns_bundle():
    inputs = build_test_inputs()
    evaluator = GlobalResearchEvaluator()

    bundle = evaluator.evaluate(inputs)

    assert isinstance(bundle, SystemMetricBundle)
    assert 0.0 <= bundle.overall_score.normalized_value() <= 10.0
    assert bundle.overall_score.grade in set(SystemHealthGrade)
    assert bundle.research_risk in set(ResearchRiskLevel)
    assert isinstance(bundle.review_required, bool)
    assert "overall_score" in bundle.score_dict()
    assert "SystemMetricBundle" in bundle.describe()


def test_intelligence_report_generator_returns_report():
    inputs = build_test_inputs()
    evaluator = GlobalResearchEvaluator()
    generator = IntelligenceReportGenerator()

    bundle = evaluator.evaluate(inputs)
    report = generator.generate(bundle)

    assert isinstance(report, IntelligenceReport)
    assert report.title == "Project ℵω Intelligence Report"
    assert report.finding_count() >= 1
    assert report.urgent_finding_count() >= 0
    assert len(report.next_actions) >= 1
    assert len(report.limitations) >= 1
    assert "Project ℵω Intelligence Report" in report.describe()


def test_report_finding_model():
    finding = ReportFinding(
        title="Test Finding",
        priority=ReportPriority.HIGH,
        explanation="Testing report finding.",
        recommended_action="Do the test action.",
    )

    assert finding.priority == ReportPriority.HIGH
    assert "Test Finding" in finding.describe()


def test_full_phase_8_pipeline():
    inputs = build_test_inputs()
    evaluator = GlobalResearchEvaluator()
    report_generator = IntelligenceReportGenerator()

    bundle = evaluator.evaluate(inputs)
    report = report_generator.generate(bundle)

    assert inputs.total_items() > 0
    assert bundle.overall_score.normalized_value() >= 0.0
    assert report.metric_bundle.overall_score.name == "Overall System Intelligence Score"
    assert report.executive_summary
    assert report.next_actions
