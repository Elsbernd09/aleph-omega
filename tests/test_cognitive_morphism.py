"""
Unit tests for Project ℵω cognitive morphism layer.

These tests verify that Phase 6 can:
- represent informal mathematical intuitions,
- convert intuitions into symbolic statements,
- generate cognitive morphisms,
- analyze formalization gaps,
- rank formalizations by quality and severity.
"""

from src.cognitive_morphism.formalizer import FormalizationDraft, InformalFormalizer
from src.cognitive_morphism.gap_analyzer import (
    FormalizationGapAnalyzer,
    FormalizationGapReport,
    GapSeverity,
    rank_gap_reports_by_quality,
    rank_gap_reports_by_severity,
)
from src.cognitive_morphism.intuition import (
    ClarityLevel,
    FormalizationRisk,
    IntuitionKind,
    IntuitionObject,
    starter_intuitions,
)
from src.cognitive_morphism.morphism import (
    CognitiveMorphism,
    CognitiveMorphismKind,
    CognitiveMorphismStatus,
    CognitivePreservation,
    example_cognitive_morphism,
)
from src.toy_topoi.statements import Statement, StatementKind, starter_statements


def test_intuition_object_scores_and_description():
    intuition = IntuitionObject(
        name="Test Intuition",
        raw_intuition="A structure should preserve identity across contexts.",
        kind=IntuitionKind.CATEGORY_STRUCTURAL,
        guiding_metaphors=["lens", "viewpoint"],
        candidate_symbols=["identity", "context", "x"],
        implied_structures=["contextual logic"],
        desired_properties=["context_sensitivity", "truth_preservation"],
        clarity_level=ClarityLevel.STRUCTURED,
        formalization_risk=FormalizationRisk.MEDIUM,
    )

    assert intuition.metaphor_count() == 2
    assert intuition.symbol_count() == 3
    assert intuition.structure_count() == 1
    assert intuition.property_count() == 2
    assert 0.0 <= intuition.conceptual_richness_score() <= 10.0
    assert 0.0 <= intuition.formalization_readiness_score() <= 10.0
    assert "Test Intuition" in intuition.describe()


def test_starter_intuitions_load():
    intuitions = starter_intuitions()

    assert len(intuitions) >= 4
    assert all(isinstance(intuition, IntuitionObject) for intuition in intuitions)


def test_cognitive_preservation_scores():
    preservation = CognitivePreservation(
        preserved_properties=["context_sensitivity"],
        lost_properties=["truth_preservation"],
        added_formal_properties=["identity", "not"],
        preserved_metaphors=["lens"],
        lost_metaphors=["viewpoint"],
    )

    assert preservation.property_preservation_score() == 5.0
    assert preservation.metaphor_preservation_score() == 5.0
    assert preservation.added_structure_count() == 2
    assert "CognitivePreservation" in preservation.describe()


def test_example_cognitive_morphism_returns_morphism():
    intuition = starter_intuitions()[0]
    statement = starter_statements()[-1]

    morphism = example_cognitive_morphism(intuition, statement)

    assert isinstance(morphism, CognitiveMorphism)
    assert morphism.source_intuition.name == intuition.name
    assert morphism.target_statement.name == statement.name
    assert morphism.kind == CognitiveMorphismKind.STRUCTURAL_EXTRACTION
    assert morphism.status in set(CognitiveMorphismStatus)
    assert 0.0 <= morphism.normalized_confidence() <= 10.0
    assert 0.0 <= morphism.normalized_meaning_drift() <= 10.0
    assert 0.0 <= morphism.formalization_quality_score() <= 10.0
    assert isinstance(morphism.requires_review(), bool)
    assert "CognitiveMorphism" in morphism.describe()


def test_informal_formalizer_creates_draft():
    formalizer = InformalFormalizer()
    intuition = starter_intuitions()[0]

    draft = formalizer.formalize(intuition)

    assert isinstance(draft, FormalizationDraft)
    assert draft.intuition.name == intuition.name
    assert isinstance(draft.statement, Statement)
    assert isinstance(draft.morphism, CognitiveMorphism)
    assert 0.0 <= draft.confidence <= 10.0
    assert isinstance(draft.requires_review, bool)
    assert "FormalizationDraft" in draft.describe()


def test_formalizer_assigns_expected_statement_kinds():
    formalizer = InformalFormalizer()

    contradiction = [
        intuition for intuition in starter_intuitions()
        if intuition.kind == IntuitionKind.CONTRADICTION_TOLERANCE
    ][0]

    modal = [
        intuition for intuition in starter_intuitions()
        if intuition.kind == IntuitionKind.MODAL_POSSIBILITY
    ][0]

    constructive = [
        intuition for intuition in starter_intuitions()
        if intuition.kind == IntuitionKind.CONSTRUCTIVE_EVIDENCE
    ][0]

    contradiction_draft = formalizer.formalize(contradiction)
    modal_draft = formalizer.formalize(modal)
    constructive_draft = formalizer.formalize(constructive)

    assert contradiction_draft.statement.kind == StatementKind.CONTRADICTION
    assert modal_draft.statement.kind == StatementKind.MODAL_CLAIM
    assert constructive_draft.statement.kind == StatementKind.THEOREM_CANDIDATE


def test_formalizer_formalize_many():
    formalizer = InformalFormalizer()
    intuitions = starter_intuitions()

    drafts = formalizer.formalize_many(intuitions)

    assert len(drafts) == len(intuitions)
    assert all(isinstance(draft, FormalizationDraft) for draft in drafts)


def test_gap_analyzer_analyzes_draft():
    formalizer = InformalFormalizer()
    analyzer = FormalizationGapAnalyzer()

    draft = formalizer.formalize(starter_intuitions()[0])
    report = analyzer.analyze_draft(draft)

    assert isinstance(report, FormalizationGapReport)
    assert report.intuition_name == draft.intuition.name
    assert report.statement_name == draft.statement.name
    assert 0.0 <= report.review_urgency_score <= 10.0
    assert 0.0 <= report.gap_index <= 10.0
    assert report.severity in set(GapSeverity)
    assert "gap_index" in report.as_dict()
    assert "FormalizationGapReport" in report.describe()


def test_gap_analyzer_analyze_many():
    formalizer = InformalFormalizer()
    analyzer = FormalizationGapAnalyzer()

    drafts = formalizer.formalize_many(starter_intuitions())
    reports = analyzer.analyze_many(drafts)

    assert len(reports) == len(drafts)
    assert all(isinstance(report, FormalizationGapReport) for report in reports)


def test_gap_ranking_helpers():
    formalizer = InformalFormalizer()
    analyzer = FormalizationGapAnalyzer()

    drafts = formalizer.formalize_many(starter_intuitions())
    reports = analyzer.analyze_many(drafts)

    by_quality = rank_gap_reports_by_quality(reports)
    by_severity = rank_gap_reports_by_severity(reports)

    assert len(by_quality) == len(reports)
    assert len(by_severity) == len(reports)

    if len(reports) >= 2:
        assert by_quality[0].gap_index <= by_quality[-1].gap_index
        assert by_severity[0].gap_index >= by_severity[-1].gap_index


def test_generated_statement_has_expected_origin_universe():
    formalizer = InformalFormalizer()

    modal_intuition = [
        intuition for intuition in starter_intuitions()
        if intuition.kind == IntuitionKind.MODAL_POSSIBILITY
    ][0]

    draft = formalizer.formalize(modal_intuition)

    assert draft.statement.origin_universe == "Modal Possibility Universe"
    assert "possible" in draft.statement.required_symbols
    assert "necessary" in draft.statement.required_symbols
