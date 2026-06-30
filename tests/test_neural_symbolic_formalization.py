"""
Unit tests for Project ℵω neural-symbolic formalization layer.

These tests verify that Phase 7 can:
- build formalization targets,
- generate Lean-style sketches,
- extract proof obligations,
- build formalization plans,
- rank plans and obligations by burden/readiness.
"""

from src.cognitive_morphism.formalization_planner import (
    FormalizationPlan,
    FormalizationPlanner,
    PlanPriority,
    PlanReadinessGrade,
    rank_plans_by_burden,
    rank_plans_by_readiness,
)
from src.cognitive_morphism.formalization_target import (
    FormalTargetKind,
    FormalizationDifficulty,
    FormalizationReadiness,
    FormalizationTarget,
    FormalizationTargetBuilder,
)
from src.cognitive_morphism.formalizer import InformalFormalizer
from src.cognitive_morphism.intuition import starter_intuitions
from src.cognitive_morphism.lean_sketch import (
    LeanSketch,
    LeanSketchGenerator,
    LeanSketchStatus,
)
from src.cognitive_morphism.proof_obligation import (
    ObligationKind,
    ObligationSeverity,
    ObligationStatus,
    ProofObligation,
    ProofObligationAnalyzer,
    ProofObligationReport,
    rank_obligation_reports_by_burden,
    rank_obligation_reports_by_readiness,
)
from src.toy_topoi.statements import StatementKind, starter_statements


def test_formalization_target_builder_creates_target():
    builder = FormalizationTargetBuilder()
    statement = starter_statements()[0]

    target = builder.build(statement)

    assert isinstance(target, FormalizationTarget)
    assert target.statement.name == statement.name
    assert target.target_kind in set(FormalTargetKind)
    assert target.difficulty in set(FormalizationDifficulty)
    assert target.readiness in set(FormalizationReadiness)
    assert 0.0 <= target.estimated_work_score() <= 10.0
    assert isinstance(target.is_ready_for_lean_sketch(), bool)
    assert "FormalizationTarget" in target.describe()


def test_target_builder_maps_statement_kinds():
    builder = FormalizationTargetBuilder()

    statements = starter_statements()
    constructive = [
        statement for statement in statements
        if statement.kind == StatementKind.THEOREM_CANDIDATE
    ][0]

    target = builder.build(constructive)

    assert target.target_kind == FormalTargetKind.THEOREM


def test_target_builder_build_many():
    builder = FormalizationTargetBuilder()
    statements = starter_statements()

    targets = builder.build_many(statements)

    assert len(targets) == len(statements)
    assert all(isinstance(target, FormalizationTarget) for target in targets)


def test_lean_sketch_generator_creates_sketch():
    builder = FormalizationTargetBuilder()
    generator = LeanSketchGenerator()

    target = builder.build(starter_statements()[0])
    sketch = generator.generate(target)

    assert isinstance(sketch, LeanSketch)
    assert sketch.target.statement.name == target.statement.name
    assert sketch.status in set(LeanSketchStatus)
    assert sketch.line_count() > 0
    assert sketch.sorry_count >= 0
    assert sketch.is_machine_checked_claim() is False
    assert "LeanSketch" in sketch.describe()


def test_lean_sketch_generator_many():
    builder = FormalizationTargetBuilder()
    generator = LeanSketchGenerator()

    targets = builder.build_many(starter_statements())
    sketches = generator.generate_many(targets)

    assert len(sketches) == len(targets)
    assert all(isinstance(sketch, LeanSketch) for sketch in sketches)


def test_proof_obligation_model():
    obligation = ProofObligation(
        name="Resolve sorry",
        kind=ObligationKind.SORRY_PLACEHOLDER,
        severity=ObligationSeverity.CRITICAL,
        status=ObligationStatus.OPEN,
        description="A sorry placeholder remains.",
        suggested_resolution="Replace sorry with a proof.",
    )

    assert obligation.severity_score() == 9.5
    assert obligation.is_blocking()
    assert "Resolve sorry" in obligation.describe()


def test_proof_obligation_analyzer_returns_report():
    builder = FormalizationTargetBuilder()
    generator = LeanSketchGenerator()
    analyzer = ProofObligationAnalyzer()

    target = builder.build(starter_statements()[2])
    sketch = generator.generate(target)
    report = analyzer.analyze(sketch)

    assert isinstance(report, ProofObligationReport)
    assert report.sketch.target.statement.name == target.statement.name
    assert report.obligation_count() >= 0
    assert report.blocking_count() >= 0
    assert 0.0 <= report.average_severity_score() <= 10.0
    assert 0.0 <= report.obligation_index() <= 10.0
    assert isinstance(report.formalization_blocked(), bool)
    assert "ProofObligationReport" in report.describe()


def test_obligation_analyzer_many_and_rankings():
    builder = FormalizationTargetBuilder()
    generator = LeanSketchGenerator()
    analyzer = ProofObligationAnalyzer()

    targets = builder.build_many(starter_statements())
    sketches = generator.generate_many(targets)
    reports = analyzer.analyze_many(sketches)

    assert len(reports) == len(sketches)

    by_burden = rank_obligation_reports_by_burden(reports)
    by_readiness = rank_obligation_reports_by_readiness(reports)

    assert len(by_burden) == len(reports)
    assert len(by_readiness) == len(reports)

    if len(reports) >= 2:
        assert by_burden[0].obligation_index() >= by_burden[-1].obligation_index()
        assert by_readiness[0].obligation_index() <= by_readiness[-1].obligation_index()


def test_formalization_planner_creates_plan():
    builder = FormalizationTargetBuilder()
    generator = LeanSketchGenerator()
    obligation_analyzer = ProofObligationAnalyzer()
    planner = FormalizationPlanner()

    target = builder.build(starter_statements()[0])
    sketch = generator.generate(target)
    report = obligation_analyzer.analyze(sketch)

    plan = planner.plan(target, sketch, report)

    assert isinstance(plan, FormalizationPlan)
    assert plan.target.statement.name == target.statement.name
    assert plan.readiness_grade in set(PlanReadinessGrade)
    assert plan.step_count() >= 1
    assert plan.urgent_step_count() >= 0
    assert 0.0 <= plan.average_step_difficulty() <= 10.0
    assert 0.0 <= plan.plan_burden_score() <= 10.0
    assert "FormalizationPlan" in plan.describe()


def test_formalization_planner_many_and_rankings():
    formalizer = InformalFormalizer()
    builder = FormalizationTargetBuilder()
    generator = LeanSketchGenerator()
    obligation_analyzer = ProofObligationAnalyzer()
    planner = FormalizationPlanner()

    drafts = formalizer.formalize_many(starter_intuitions())
    targets = builder.build_many([draft.statement for draft in drafts])
    sketches = generator.generate_many(targets)
    reports = obligation_analyzer.analyze_many(sketches)
    plans = planner.plan_many(targets, sketches, reports)

    assert len(plans) == len(targets)

    by_burden = rank_plans_by_burden(plans)
    by_readiness = rank_plans_by_readiness(plans)

    assert len(by_burden) == len(plans)
    assert len(by_readiness) == len(plans)

    if len(plans) >= 2:
        assert by_burden[0].plan_burden_score() >= by_burden[-1].plan_burden_score()
        assert by_readiness[0].plan_burden_score() <= by_readiness[-1].plan_burden_score()


def test_full_phase_7_pipeline_from_intuitions():
    formalizer = InformalFormalizer()
    builder = FormalizationTargetBuilder()
    generator = LeanSketchGenerator()
    obligation_analyzer = ProofObligationAnalyzer()
    planner = FormalizationPlanner()

    drafts = formalizer.formalize_many(starter_intuitions())
    statements = [draft.statement for draft in drafts]
    targets = builder.build_many(statements)
    sketches = generator.generate_many(targets)
    reports = obligation_analyzer.analyze_many(sketches)
    plans = planner.plan_many(targets, sketches, reports)

    assert len(drafts) == len(starter_intuitions())
    assert len(targets) == len(drafts)
    assert len(sketches) == len(targets)
    assert len(reports) == len(sketches)
    assert len(plans) == len(reports)

    assert all(plan.step_count() >= 1 for plan in plans)
    assert all(plan.next_action for plan in plans)


def test_plan_has_valid_priorities():
    formalizer = InformalFormalizer()
    builder = FormalizationTargetBuilder()
    generator = LeanSketchGenerator()
    obligation_analyzer = ProofObligationAnalyzer()
    planner = FormalizationPlanner()

    draft = formalizer.formalize(starter_intuitions()[0])
    target = builder.build(draft.statement)
    sketch = generator.generate(target)
    report = obligation_analyzer.analyze(sketch)
    plan = planner.plan(target, sketch, report)

    assert all(step.priority in set(PlanPriority) for step in plan.steps)
